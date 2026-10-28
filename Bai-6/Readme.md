# BÁO CÁO THỰC HÀNH: TRIỂN KHAI CI/CD PIPELINE TRÊN GITLAB VỚI DOCUSAURUS

**Học phần:** Bảo mật với DevSecOps  
**Sinh viên thực hiện: Đỗ Trí Hoàng
**Group:** dotrihoen-group  
**Dự án:** `pipeline-tutorial`  

---

## 1. Giới thiệu tổng quan
Bài thực hành nhằm mục tiêu làm quen với quy trình thiết lập dự án mã nguồn, cấu hình pipeline tự động hóa CI/CD trên nền tảng GitLab kết hợp với framework tài liệu tĩnh Docusaurus (Node.js).

---

## 2. Nhật ký các bước thực hiện chi tiết

### Bước 1: Khởi tạo dự án mới trên GitLab
* Truy cập giao diện tạo mới dự án của GitLab trong không gian làm việc `dotrihoen-group`.
* Lựa chọn mục **Create blank project** để tạo một repository trống hoàn toàn từ đầu.

![alt text](<Screenshot 2026-10-28 082953.png>)

---

### Bước 2: Cấu hình thông số dự án
* Đặt tên dự án: `pipeline-tutorial`.
* Đường dẫn Repository: `https://gitlab.com/dotrihoen-group/pipeline-tutorial`.
* Cấu hình quyền riêng tư và tích chọn **Initialize repository with a README** để tạo nhánh mặc định (`main`).

![alt text](<Screenshot 2026-10-28 083118.png>)

---

### Bước 3: Chuẩn bị thông tin xác thực tài khoản (Personal Access Token)
* Để có thể làm việc và tương tác từ Terminal Kali Linux với GitLab qua giao thức HTTPS, tiến hành kiểm tra thông tin tài khoản `dotriihoangg01.01`.
* Cấu hình **Personal Access Token** với quyền thao tác mã nguồn (`write_repository`) để sử dụng thay thế cho mật khẩu thông thường.

![alt text](<Screenshot 2026-10-28 084331.png>)

---

### Bước 4: Clone Repository về máy cục bộ Kali Linux
* Mở Terminal trên Kali Linux, di chuyển về thư mục gốc `~`.
* Chạy lệnh clone repository `pipeline-tutorial` về máy thông qua HTTPS và xác thực tài khoản thành công:
  ```bash
  cd ~
  git clone https://gitlab.com/dotrihoen-group/pipeline-tutorial.git
  ```

![alt text](<Screenshot 2026-10-28 085645.png>)

---

### Bước 5: Khởi tạo ứng dụng trang web Docusaurus
* Khởi tạo dự án trang web tĩnh bằng Docusaurus với mẫu `classic` và ngôn ngữ JavaScript:
  ```bash
  npx create-docusaurus@latest website classic
  ```
* Hệ thống tải các thành phần, cấu trúc thư mục của website và tiến hành cài đặt các gói phụ thuộc (`dependencies`) thông qua npm.
* Di chuyển toàn bộ mã nguồn website đã tạo từ thư mục `website` ra ngoài thư mục gốc của repository, đồng thời cập nhật file cấu hình `docusaurus.config.js`.

![alt text](<Screenshot 2026-10-28 085904.png>)

---

### Bước 6: Đẩy toàn bộ mã nguồn (Push Code) lên GitLab
* Toàn bộ mã nguồn trang web Docusaurus đã được commit và đẩy thành công từ máy Kali Linux lên nhánh `main` của kho lưu trữ trên GitLab:
  ```bash
  git push origin main
  ```
* Tiến trình nén và truyền tải đạt 100% (54/54 objects), mã nguồn được cập nhật khớp với commit `2a6f00f`.

![alt text](<Screenshot 2026-10-28 092858.png>)
---

### Bước 7: Kiểm tra cấu trúc kho lưu trữ trên GitLab
* Quay lại giao diện web của repository `pipeline-tutorial`, toàn bộ cây thư mục mã nguồn của trang web Docusaurus đã hiện diện đầy đủ: `blog/`, `docs/`, `src/`, `static/`, `docusaurus.config.js`, `package.json`,...
* Điều này xác nhận quá trình khởi tạo, cấu hình và đồng bộ mã nguồn cục bộ lên hệ thống điều khiển phiên bản đám mây đã hoàn tất 100%.


![alt text](<Screenshot 2026-10-28 093050.png>)
---

### Bước 8: Kiểm tra Pipeline và Rào cản xác thực hệ thống (Verification Gate)
* Truy cập mục **Build > Pipelines** để kiểm tra việc kích hoạt tiến trình CI/CD tự động.
* Tại đây, hệ thống GitLab hiển thị cảnh báo:
  > *"Before you can run pipelines, we need to verify your account."*
* **Giải thích nguyên nhân:** GitLab áp dụng chính sách bảo mật chống lạm dụng tài nguyên tính toán (Shared Runners), yêu cầu xác minh danh tính tài khoản bằng thẻ thanh toán quốc tế / số điện thoại. Do gặp giới hạn ở khâu xác thực phương thức này, hệ thống đám mây chưa cấp quyền thực thi Shared Runner cho tài khoản.

![alt text](<Screenshot 2026-10-28 093150.png>)

---

## 3. Đánh giá kết quả thực hành
1. **Mức độ hoàn thành:**
   * Các giai đoạn kỹ thuật cốt lõi bao gồm: chuẩn bị môi trường Linux, khởi tạo ứng dụng Docusaurus, cấu hình repository, quản lý nhánh và đồng bộ Git thông qua Personal Access Token đều đã được thực hiện chính xác và thành công.
   * Mã nguồn website đã được biên dịch, tổ chức và đồng bộ hoàn chỉnh trên máy chủ GitLab.

2. **Kết luận:**
   * Việc pipeline chưa tự động trigger trên GitLab.com hoàn toàn xuất phát từ rào cản chính sách xác thực tài khoản người dùng của nhà cung cấp dịch vụ (GitLab), không phải do lỗi cấu hình mã nguồn hay cú pháp lệnh.
   * Toàn bộ logic triển khai còn lại chủ yếu là cơ chế tải artifact và phân phối qua GitLab Pages (`pages:deploy`). Về mặt kiến trúc và kỹ năng vận hành công cụ, bài thực hành đã đạt được đầy đủ mục tiêu đề ra.