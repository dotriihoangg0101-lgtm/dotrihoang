# LAB 3 – Xây dựng Secure Validator và Secure Logger

## 1. Giới thiệu

Trong Lab 3, em xây dựng một ứng dụng Flask đơn giản kết hợp hai thành phần chính là **Secure Validator** và **Secure Logger**.

Mục đích của bài là thực hành một số kỹ thuật bảo vệ dữ liệu đầu vào và ghi log an toàn. Ứng dụng nhận dữ liệu từ API `/validate`, sau đó kiểm tra email, URL, tên file và xử lý một số dữ liệu có nguy cơ liên quan đến SQL Injection hoặc XSS.

Bên cạnh đó, hệ thống còn có cơ chế che thông tin nhạy cảm trong log, ghi log theo định dạng JSON, xoay vòng file log và tạo chữ ký SHA-256 cho từng dòng log.

## 2. Mục tiêu

Các mục tiêu chính của Lab 3:

- Xây dựng API bằng Flask.
- Kiểm tra định dạng email.
- Kiểm tra URL cơ bản.
- Ngăn chặn một số trường hợp path traversal qua tên file.
- Làm sạch dữ liệu đầu vào liên quan đến SQL.
- Escape dữ liệu HTML để hạn chế XSS.
- Che một số thông tin cá nhân hoặc secret trước khi ghi log.
- Ghi log dưới dạng JSON.
- Giới hạn kích thước file log và thực hiện rotation.
- Tạo hash SHA-256 cho nội dung log để hỗ trợ kiểm tra tính toàn vẹn.

## 3. Cấu trúc thư mục

```text
LAb-3/
├── app.py
├── requirements.txt
├── secure.log
├── secure.log.sig
├── securelogger/
│   ├── __init__.py
│   └── logger.py
└── securevalidator/
    ├── __init__.py
    └── core.py
```

Trong đó:

- `app.py`: ứng dụng Flask và API `/validate`.
- `securevalidator/core.py`: các hàm kiểm tra và xử lý dữ liệu đầu vào.
- `securelogger/logger.py`: xây dựng hệ thống log an toàn.
- `secure.log`: file lưu log.
- `secure.log.sig`: lưu hash SHA-256 của từng dòng log.
- `requirements.txt`: chứa thư viện Flask.

## 4. Secure Validator

### 4.1. Kiểm tra email

Hàm:

```python
validate_email(email)
```

sử dụng regular expression để kiểm tra email có dạng cơ bản:

```text
username@domain.tld
```

Hàm trả về `True` nếu phù hợp và `False` nếu không phù hợp.

Đây là kiểm tra định dạng cơ bản, không phải kiểm tra xem địa chỉ email có thực sự tồn tại hay không.

### 4.2. Kiểm tra URL

Hàm:

```python
validate_url(url)
```

sử dụng `urllib.parse` để phân tích URL.

Trong bài, URL được chấp nhận khi:

- Scheme là `http` hoặc `https`.
- Có `netloc`.

Ví dụ:

```text
https://secure.com
```

được xem là URL hợp lệ.

Phần này mới chỉ thực hiện kiểm tra URL ở mức cơ bản và chưa phải cơ chế SSRF protection đầy đủ.

### 4.3. Kiểm tra tên file

Hàm:

```python
validate_filename(filename)
```

được sử dụng để hạn chế path traversal.

Các chuỗi như:

```text
..
/
\
```

sẽ bị từ chối.

Ví dụ một tên file bình thường:

```text
report.pdf
```

được chấp nhận, trong khi tên file có dấu hiệu truy cập sang thư mục khác sẽ bị từ chối.

### 4.4. Làm sạch SQL input

Hàm:

```python
sanitize_sql_input(input_str)
```

loại bỏ một số ký tự và từ khóa thường xuất hiện trong các payload SQL Injection, chẳng hạn:

```text
--
;
'
"
#
OR
AND
SELECT
DROP
UNION
```

Ví dụ dữ liệu:

```text
OR 1=1 --
```

sau khi xử lý trong kết quả mẫu trở thành:

```text
1=1
```

Cách làm này phù hợp với mục đích minh họa của bài lab, nhưng trong ứng dụng thực tế không nên chỉ dựa vào việc xóa chuỗi để chống SQL Injection. Nên sử dụng parameterized queries hoặc prepared statements.

### 4.5. Xử lý HTML

Hàm:

```python
sanitize_html_input(html_str)
```

sử dụng:

```python
html.escape()
```

để chuyển các ký tự HTML đặc biệt thành dạng escaped.

Ví dụ:

```html
<script>alert(1)</script>
```

được chuyển thành dạng:

```text
&lt;script&gt;alert(1)&lt;/script&gt;
```

Việc này giúp dữ liệu được xử lý như văn bản thay vì HTML/JavaScript trong những ngữ cảnh phù hợp.

## 5. Secure Logger

### 5.1. Che thông tin nhạy cảm

Trong `securelogger/logger.py`, hàm:

```python
mask_pii()
```

được sử dụng để tìm và che một số thông tin như:

- Email.
- Token.
- API key.
- Key.
- Password.

Ví dụ email có thể được chuyển thành:

```text
<email_masked>
```

Mục đích là hạn chế việc thông tin nhạy cảm xuất hiện trực tiếp trong file log.

### 5.2. Log dạng JSON

Hệ thống sử dụng `JSONFormatter` để tạo log theo dạng JSON.

Ví dụ một bản ghi có cấu trúc:

```json
{
  "timestamp": "...",
  "level": "INFO",
  "message": "Validation check performed",
  "data": "...",
  "results": "..."
}
```

Cách lưu này giúp log có cấu trúc rõ ràng và thuận tiện hơn khi muốn xử lý bằng các công cụ phân tích log.

### 5.3. Hash log

Sau khi ghi log, hệ thống sử dụng SHA-256:

```python
hashlib.sha256(line.encode('utf-8')).hexdigest()
```

để tạo hash cho từng dòng log.

Các hash được lưu trong:

```text
secure.log.sig
```

Mục đích của phần này là hỗ trợ kiểm tra xem nội dung log có bị thay đổi hay không.

### 5.4. Log rotation

Hệ thống sử dụng `RotatingFileHandler` với giới hạn:

```text
MAX_LOG_SIZE = 1024 * 1024
BACKUP_COUNT = 2
```

Tức là file log được giới hạn khoảng 1 MB và có tối đa 2 bản backup theo cấu hình hiện tại.

Khi rotation xảy ra, file cũ được nén bằng GZip.

## 6. API `/validate`

Ứng dụng Flask cung cấp endpoint:

```text
POST /validate
```

API nhận dữ liệu JSON và thực hiện các kiểm tra:

```text
email
url
filename
sql
html
```

Ví dụ request:

```json
{
  "email": "student@example.com",
  "url": "https://secure.com",
  "filename": "report.pdf",
  "sql": "OR 1=1 --",
  "html": "<script>alert(1)</script>"
}
```

API trả về kết quả kiểm tra tương ứng.

## 7. Luồng xử lý

Có thể mô tả luồng hoạt động của Lab 3 như sau:

```text
Client
  |
  | POST /validate
  v
Flask Application
  |
  +----> Validate Email
  |
  +----> Validate URL
  |
  +----> Validate Filename
  |
  +----> Sanitize SQL
  |
  +----> Escape HTML
  |
  v
Secure Logger
  |
  +----> Mask dữ liệu nhạy cảm
  |
  +----> Format JSON
  |
  +----> Ghi secure.log
  |
  +----> Tạo SHA-256 signature
  |
  v
JSON Response
```

## 8. Cài đặt

Cài các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

Sau đó chạy:

```bash
python app.py
```

Ứng dụng Flask sẽ khởi động ở chế độ debug theo cấu hình trong `app.py`.

## 9. Kết quả thực tế

Trong file `secure.log` đã có một bản ghi kiểm thử.

Một số kết quả đáng chú ý:

- Email được che thành `<email_masked>`.
- URL `https://secure.com` được xác nhận hợp lệ.
- `report.pdf` được xác nhận là tên file hợp lệ.
- Chuỗi SQL mẫu `OR 1=1 --` được xử lý thành `1=1`.
- HTML `<script>alert(1)</script>` được escape thành dạng HTML entity.

File:

```text
secure.log.sig
```

cũng chứa hash SHA-256 tương ứng với log được tạo.

## 10. Một số điểm cần lưu ý

Các cơ chế trong bài chủ yếu nhằm mục đích học tập và minh họa.

Ví dụ:

- Kiểm tra URL hiện tại chưa phải biện pháp chống SSRF đầy đủ.
- Việc xóa từ khóa SQL không thay thế cho parameterized query.
- Regular expression kiểm tra email chỉ kiểm tra định dạng cơ bản.
- Việc lưu hash log giúp phát hiện thay đổi khi có cơ chế đối chiếu hash phù hợp, nhưng bản thân file `.sig` nếu bị sửa cùng với log thì chưa đủ để đảm bảo tính toàn vẹn tuyệt đối.
- Ứng dụng đang sử dụng `debug=True`, vì vậy khi triển khai thực tế cần cấu hình khác để tránh các rủi ro không cần thiết.

## 11. Nhận xét

Qua Lab 3, em hiểu rõ hơn rằng bảo mật không chỉ nằm ở việc kiểm tra dữ liệu đầu vào mà còn liên quan đến cách hệ thống ghi nhận và bảo vệ thông tin trong log.

Phần `securevalidator` giúp kiểm soát dữ liệu đầu vào trước khi xử lý, còn `securelogger` tập trung vào việc giảm nguy cơ làm lộ thông tin nhạy cảm và hỗ trợ kiểm tra tính toàn vẹn của log.

Điểm em thấy đáng chú ý là hai thành phần này có thể tách riêng thành module để sử dụng lại trong những ứng dụng khác.

## 12. Kết luận

Lab 3 giúp em thực hành xây dựng một API có một số lớp kiểm tra bảo mật cơ bản. Qua quá trình làm, em hiểu thêm về validation, sanitization, XSS, SQL Injection, path traversal và secure logging.

Mặc dù các giải pháp trong bài chưa thể thay thế các cơ chế bảo mật chuyên sâu khi triển khai thực tế, chúng giúp em có cái nhìn rõ hơn về cách đưa các bước kiểm tra bảo mật vào một ứng dụng Python/Flask.
