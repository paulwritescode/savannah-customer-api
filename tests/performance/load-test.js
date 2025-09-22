import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10, // 10 virtual users
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
    http_req_failed: ['rate<0.01'], // Error rate must be below 1%
  },
};

const API_URL = __ENV.API_URL || 'http://localhost:8000';

export function setup() {
  // Create test data
  const authToken = 'Bearer test-token'; // Replace with actual auth logic
  return { authToken };
}

export default function (data) {
  const headers = {
    'Authorization': data.authToken,
    'Content-Type': 'application/json',
  };

  // Test health endpoint
  let response = http.get(`${API_URL}/health`);
  check(response, {
    'health check status is 200': (r) => r.status === 200,
  });

  sleep(1);

  // Test customers endpoint
  response = http.get(`${API_URL}/api/v1/customers/`, { headers });
  check(response, {
    'customers list status is 200 or 401': (r) => [200, 401].includes(r.status),
  });

  sleep(1);

  // Test orders endpoint
  response = http.get(`${API_URL}/api/v1/orders/`, { headers });
  check(response, {
    'orders list status is 200 or 401': (r) => [200, 401].includes(r.status),
  });

  sleep(1);
}

export function teardown(data) {
  // Clean up test data if needed
}
