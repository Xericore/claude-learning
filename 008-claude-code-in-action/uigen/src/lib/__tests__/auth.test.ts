// @vitest-environment node
import { describe, test, expect, vi, beforeEach } from "vitest";
import { jwtVerify } from "jose";

const { cookiesMock, setMock } = vi.hoisted(() => {
  const setMock = vi.fn();
  const cookiesMock = vi.fn(async () => ({ set: setMock }));
  return { cookiesMock, setMock };
});

vi.mock("server-only", () => ({}));
vi.mock("next/headers", () => ({ cookies: cookiesMock }));

import { createSession } from "../auth";

const SEVEN_DAYS_MS = 7 * 24 * 60 * 60 * 1000;

beforeEach(() => {
  setMock.mockClear();
  cookiesMock.mockClear();
});

describe("createSession", () => {
  test("sets an auth-token cookie with the expected options", async () => {
    const before = Date.now();
    await createSession("user-1", "user@example.com");
    const after = Date.now();

    expect(setMock).toHaveBeenCalledTimes(1);
    const [name, token, options] = setMock.mock.calls[0];

    expect(name).toBe("auth-token");
    expect(typeof token).toBe("string");
    expect(options.httpOnly).toBe(true);
    expect(options.sameSite).toBe("lax");
    expect(options.path).toBe("/");
    expect(options.secure).toBe(false);

    const expiresAtMs = options.expires.getTime();
    expect(expiresAtMs).toBeGreaterThanOrEqual(before + SEVEN_DAYS_MS - 1000);
    expect(expiresAtMs).toBeLessThanOrEqual(after + SEVEN_DAYS_MS + 1000);
  });

  test("signs a JWT containing the userId, email, and expiresAt", async () => {
    await createSession("user-1", "user@example.com");

    const [, token, options] = setMock.mock.calls[0];
    const secret = new TextEncoder().encode(
      process.env.JWT_SECRET || "development-secret-key"
    );
    const { payload } = await jwtVerify(token, secret);

    expect(payload.userId).toBe("user-1");
    expect(payload.email).toBe("user@example.com");
    expect(new Date(payload.expiresAt as string).getTime()).toBe(
      options.expires.getTime()
    );
  });

  test("produces a token that expires roughly 7 days from now", async () => {
    await createSession("user-1", "user@example.com");

    const [, token] = setMock.mock.calls[0];
    const secret = new TextEncoder().encode(
      process.env.JWT_SECRET || "development-secret-key"
    );
    const { payload } = await jwtVerify(token, secret);

    expect(payload.exp).toBeDefined();
    expect(payload.iat).toBeDefined();
    const durationSeconds = (payload.exp as number) - (payload.iat as number);
    expect(durationSeconds).toBeGreaterThanOrEqual(SEVEN_DAYS_MS / 1000 - 5);
    expect(durationSeconds).toBeLessThanOrEqual(SEVEN_DAYS_MS / 1000 + 5);
  });
});
