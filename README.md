# SECURE VALIDATOR LAB

## 1. Thông tin bài thực hành

**Tên bài:** Secure Validator Lab  
**Mục tiêu:** Xây dựng và kiểm thử các cơ chế kiểm tra, làm sạch dữ liệu đầu vào cho ứng dụng Web bằng Python Flask.

Bài thực hành tập trung vào 5 nhóm dữ liệu đầu vào:

1. Email Validation
2. URL Validation
3. Filename / Path Traversal Validation
4. SQL Input Sanitization
5. HTML Input Sanitization

Ngoài việc xây dựng chức năng, bài thực hành sử dụng **Unit Test** để kiểm tra kết quả của từng chức năng.

---

## 2. Mục tiêu

Bài thực hành nhằm:

- Thực hành xây dựng các hàm kiểm tra dữ liệu đầu vào.
- Nhận biết các trường hợp dữ liệu bất thường có thể gây rủi ro bảo mật.
- Sử dụng Unit Test để kiểm chứng chức năng.
- Phân tích trường hợp kiểm thử đạt và không đạt.
- Nhận biết hạn chế của các phương pháp kiểm tra bằng Regex và Blacklist.
- Đề xuất hướng cải thiện khi triển khai trong hệ thống thực tế.

---

## 3. Công nghệ sử dụng

- **Python 3**
- **Flask**
- **unittest**
- **Regular Expression (Regex)**
- **HTML**

---

## 4. Cấu trúc chương trình

```text
secure-validator-lab/
├── app.py
├── requirements.txt
├── README.md
│
├── securevalidator/
│   ├── __init__.py
│   └── core.py
│
├── templates/
│   └── index.html
│
└── tests/
    └── test_validators.py
```

### Chức năng các file

| File | Chức năng |
|---|---|
| `app.py` | Khởi chạy Flask và xử lý dữ liệu từ giao diện Web |
| `securevalidator/core.py` | Chứa các hàm validate và sanitize |
| `securevalidator/__init__.py` | Export các hàm sử dụng trong chương trình |
| `templates/index.html` | Giao diện nhập dữ liệu |
| `tests/test_validators.py` | Unit Test cho các chức năng |
| `requirements.txt` | Danh sách thư viện cần cài đặt |

---

## 5. Các chức năng thực hiện

### 5.1. Email Validation

Hàm:

```python
validate_email(email)
```

Kiểm tra định dạng Email bằng Regex.

Ví dụ kiểm thử:

```text
user@example.com
user@exam..ple.com
```

Mục đích là kiểm tra khả năng nhận biết Email hợp lệ và một số Email có định dạng bất thường.

---

### 5.2. URL Validation

Hàm:

```python
validate_url(url)
```

Kiểm tra URL có sử dụng giao thức `http` hoặc `https` và có phần địa chỉ mạng.

Ví dụ:

```text
https://example.com
http://localhost
```

Kiểm thử này được sử dụng để đánh giá giới hạn của cơ chế kiểm tra URL hiện tại.


---

### 5.3. Filename / Path Traversal Validation

Hàm:

```python
validate_filename(filename)
```

Kiểm tra tên file và từ chối một số biểu diễn đường dẫn có thể liên quan đến Path Traversal.

Ví dụ:

```text
report.pdf
../../etc/passwd
```

Mục tiêu là kiểm tra việc xử lý dữ liệu tên file trước khi sử dụng trong thao tác với hệ thống tệp.

---

### 5.4. SQL Input Sanitization

Hàm:

```python
sanitize_sql_input(input_str)
```

Loại bỏ một số ký tự và từ khóa SQL thường gặp.

Ví dụ kiểm thử:

```text
admin'OR1=1
```

Mục tiêu của bài thực hành là quan sát giới hạn của phương pháp blacklist.

**Hướng triển khai thực tế:** Nên sử dụng Prepared Statement / Parameterized Query thay vì phụ thuộc vào việc xóa từ khóa SQL.

---

### 5.5. HTML Input Sanitization

Hàm:

```python
sanitize_html_input(html_str)
```

Sử dụng `html.escape()` để escape các ký tự HTML đặc biệt.

Ví dụ:

```html
<script>alert(1)</script>
```

Mục tiêu là hạn chế việc dữ liệu người dùng được trình duyệt hiểu trực tiếp như HTML.

**Lưu ý:** Trong ứng dụng thực tế cần kết hợp output encoding phù hợp với từng ngữ cảnh và các cơ chế bảo vệ bổ sung như CSP.

---

## 6. Unit Test

File:

```text
tests/test_validators.py
```

Chương trình hiện có **10 test case** cho 5 nhóm chức năng.

| Nhóm | Nội dung |
|---|---|
| Email | Kiểm tra Email hợp lệ và bất thường |
| URL | Kiểm tra URL hợp lệ và URL nội bộ |
| Filename | Kiểm tra Filename và Path Traversal |
| SQL | Kiểm tra chuỗi SQL bất thường và dữ liệu thông thường |
| HTML | Kiểm tra dữ liệu chứa Script và dữ liệu thông thường |

### Chạy Unit Test

Tại thư mục project:

```powershell
cd D:\Do_An_MOnHoc\TH-AnNinhThongTin\secure-validator-lab
```

Chạy:

```powershell
..venv\Scripts\python.exe -m unittest discover tests -v
```

Kết quả kiểm thử dự kiến:

```text
Ran 10 tests
```

Ký hiệu:

```text
. = PASS
F = FAIL
E = ERROR
```

Một test PASS chỉ có nghĩa là **kết quả thực tế phù hợp với điều kiện mà test đặt ra**.

---

## 7. Chạy ứng dụng Web

Khởi động Flask:

```powershell
..venv\Scripts\python.exe app.py
```

Sau đó truy cập:

```text
http://127.0.0.1:5000
```

Giao diện Web cho phép nhập dữ liệu và quan sát kết quả của các hàm validation/sanitization.

---

## 8. Kết quả và nhận xét

Qua quá trình kiểm thử, có thể nhận thấy:

### Email

Regex hiện tại chỉ thực hiện kiểm tra định dạng cơ bản nên chưa bao phủ đầy đủ các trường hợp Email bất thường.

### URL

Kiểm tra `http/https` và `netloc` chỉ xác nhận cú pháp ở mức cơ bản, chưa đủ để xây dựng cơ chế chống SSRF hoàn chỉnh.

### Filename

Kiểm tra ký tự đường dẫn giúp hạn chế một số trường hợp Path Traversal nhưng cần kết hợp với chuẩn hóa đường dẫn và giới hạn thư mục được phép truy cập.

### SQL

Blacklist có thể bỏ sót nhiều cách biểu diễn đầu vào. Trong ứng dụng thực tế nên dùng Parameterized Query / Prepared Statement.

### HTML

Escape dữ liệu HTML giúp giảm nguy cơ XSS trong ngữ cảnh HTML phù hợp. Tuy nhiên cần kết hợp với các biện pháp bảo vệ bổ sung tùy theo ngữ cảnh sử dụng dữ liệu.

---

## 9. Kết luận

Bài thực hành đã xây dựng một ứng dụng Flask đơn giản có chức năng kiểm tra và xử lý dữ liệu đầu vào, đồng thời xây dựng Unit Test để kiểm chứng các chức năng.

Qua bài lab, có thể thấy rằng **input validation và sanitization có vai trò quan trọng trong bảo mật ứng dụng Web**, nhưng các phương pháp đơn giản dựa trên Regex hoặc Blacklist không nên được xem là cơ chế bảo vệ duy nhất trong môi trường thực tế.
