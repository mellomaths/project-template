import { sum } from "../src/main";

test("It should sum 2+2", function () {
  const result = sum(2, 2);
  expect(result).toBe(4);
});
