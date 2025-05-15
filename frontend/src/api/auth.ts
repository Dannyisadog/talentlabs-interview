import { post } from "../utils/httpClient";

export const fakeLogin = async (): Promise<{
  access_token: string;
}> => {
  return post("auth/fake-login");
};