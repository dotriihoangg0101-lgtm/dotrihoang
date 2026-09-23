# LAB 2 – Xây dựng Git Pre-Commit Hook kiểm tra an toàn mã nguồn

## 1. Giới thiệu

Trong Lab 2, em thực hiện xây dựng một **Git pre-commit hook** có tên là `GitSecure`. Mục đích của hook là kiểm tra mã nguồn trước khi commit vào Git, từ đó phát hiện một số vấn đề bảo mật cơ bản như thông tin nhạy cảm bị đưa vào mã nguồn, file có quyền ghi không an toàn và một số lỗi bảo mật được Bandit phát hiện.

Ý tưởng của bài là thực hiện kiểm tra ngay tại thời điểm `git commit`. Nếu phát hiện vấn đề, quá trình commit sẽ bị dừng lại để người dùng kiểm tra và xử lý trước khi tiếp tục.

## 2. Mục tiêu

Các mục tiêu chính của Lab 2:

- Làm quen với cơ chế **Git hook**, cụ thể là `pre-commit`.
- Kiểm tra thông tin nhạy cảm trong các file chuẩn bị commit.
- Kiểm tra quyền ghi file trên hệ điều hành Linux.
- Sử dụng **Bandit** để kiểm tra một số vấn đề bảo mật trong mã Python.
- Ghi lại các phát hiện vào file `gitsecure.log`.
- Thực hiện kiểm thử bằng một file Python có chứa mật khẩu.

## 3. Cấu trúc thư mục

```text
LAb-2/
├── .githooks/
│   └── pre-commit
├── pre-commit-hook-test/
│   └── bad.py
└── requirements.txt
```

Trong đó:

- `.githooks/pre-commit`: file hook thực hiện các bước kiểm tra trước khi commit.
- `pre-commit-hook-test/bad.py`: file dùng để kiểm thử trường hợp có thông tin nhạy cảm.
- `requirements.txt`: chứa thư viện `bandit`.

## 4. Các chức năng chính

### 4.1. Phát hiện thông tin nhạy cảm

Hook sử dụng biểu thức chính quy để tìm một số dạng thông tin có thể là bí mật, ví dụ:

- API key
- Secret
- Password
- Token
- Một số dạng AWS Access Key

Ví dụ file kiểm thử:

```python
password = "654321"
```

Đây là dữ liệu được cố tình đưa vào để kiểm tra khả năng phát hiện của hook.

### 4.2. Kiểm tra quyền của file

Trên Linux, chương trình kiểm tra xem file có quyền **world-writable** hay không.

Nếu file cho phép mọi người có quyền ghi, hook sẽ tạo cảnh báo vì đây có thể là một cấu hình quyền không an toàn.

Phần kiểm tra này được bỏ qua trên Windows do cách quản lý quyền file giữa Windows và Linux khác nhau.

### 4.3. Kiểm tra bằng Bandit

Hook chạy lệnh:

```bash
bandit -r .
```

Bandit là công cụ phân tích mã nguồn Python để tìm các vấn đề bảo mật phổ biến.

Nếu phát hiện vấn đề có mức độ `High`, hook sẽ ghi nhận phát hiện và chặn commit.

Nếu Bandit chưa được cài đặt, hook cũng thông báo để người dùng có thể cài bằng:

```bash
pip install bandit
```

## 5. Cơ chế hoạt động

Quá trình xử lý của hook có thể hiểu đơn giản như sau:

```text
git commit
    |
    v
Pre-commit Hook
    |
    +----> Đọc danh sách file staged
    |
    +----> Quét thông tin nhạy cảm
    |
    +----> Kiểm tra quyền file
    |
    +----> Chạy Bandit
    |
    v
Có phát hiện?
   / \
  Có  Không
  |      |
  v      v
Chặn   Cho phép
commit commit
```

## 6. Ghi log

Khi phát hiện vấn đề, chương trình ghi thông tin vào:

```text
gitsecure.log
```

Mỗi dòng log có thời gian phát hiện và nội dung vấn đề. Điều này giúp có thể xem lại các lần kiểm tra trước đó.

## 7. Cách cài đặt

Trước tiên cài thư viện cần thiết:

```bash
pip install -r requirements.txt
```

Nếu sử dụng Git hook trong thư mục `.githooks`, có thể cấu hình Git sử dụng thư mục này bằng:

```bash
git config core.hooksPath .githooks
```

Sau đó kiểm tra:

```bash
git config --get core.hooksPath
```

Kết quả mong muốn:

```text
.githooks
```

## 8. Kiểm thử

Trong thư mục kiểm thử có file:

```text
pre-commit-hook-test/bad.py
```

Nội dung:

```python
password = "654321"
```

Sau khi đưa file vào staging:

```bash
git add .
```

và thực hiện:

```bash
git commit -m "test security hook"
```

Hook sẽ quét các file đang staged. Nếu phát hiện thông tin nhạy cảm, quá trình commit sẽ bị chặn và màn hình sẽ hiển thị thông báo:

```text
COMMIT BLOCKED by GitSecure:
```

Điều này cho thấy hook có thể kiểm tra mã nguồn trước khi dữ liệu được commit vào repository.

## 9. Kết quả đạt được

Qua bài thực hành, em đã hiểu được cách sử dụng Git hook để thực hiện một bước kiểm tra bảo mật tự động trước khi commit.

Cụ thể, chương trình có thể:

- Quét các file đang chuẩn bị commit.
- Phát hiện một số mẫu thông tin nhạy cảm.
- Kiểm tra quyền file trên Linux.
- Kết hợp Bandit để kiểm tra mã Python.
- Chặn commit khi phát hiện vấn đề.
- Ghi lại kết quả vào log.

## 10. Nhận xét

Theo em, cách làm này phù hợp để đưa một số bước kiểm tra bảo mật vào quá trình phát triển phần mềm. Điểm dễ thấy nhất là lỗi có thể được phát hiện sớm thay vì chờ đến lúc code đã được đưa lên repository.

Tuy nhiên, các biểu thức chính quy trong bài chỉ nhận diện được một số mẫu phổ biến nên không thể đảm bảo phát hiện tất cả loại secret. Ngoài ra, việc kiểm tra hiện tại chủ yếu là kiểm tra ở phía máy phát triển, nên trong dự án thực tế vẫn nên kết hợp thêm CI/CD và các công cụ quản lý secret.

## 11. Kết luận

Lab 2 giúp em hiểu rõ hơn về Git pre-commit hook và cách kết hợp kiểm tra bảo mật vào quy trình commit. Đây là một bước cơ bản nhưng có ý nghĩa trong việc xây dựng quy trình phát triển phần mềm an toàn hơn.
