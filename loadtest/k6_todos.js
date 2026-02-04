import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 10,           // 10 concurrent users
  duration: "30s",   // 30-second test

  thresholds: {
    http_req_duration: ["p(95)<500"],  // 95% under 500ms
  },
};

export default function () {
  // Simulate user loading the app
  let res = http.get("http://host.docker.internal:5000/");
  check(res, { "landing page 200": (r) => r.status === 200 });

  // Simulate frontend calling the API
  res = http.get("http://host.docker.internal:5000/api/todos");
  check(res, { "api todos 200": (r) => r.status === 200 });

  sleep(1);
}
