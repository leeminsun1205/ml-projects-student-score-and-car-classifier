# Đồ án cuối kỳ môn Nhập môn Lập trình - Dự đoán kết quả học tập từ dữ liệu WeCode

**Mục tiêu chung:** Dự đoán kết quả học tập môn Nhập môn Lập trình (IT001) dựa trên dữ liệu nộp bài của sinh viên trên nền tảng WeCode.

**Dữ liệu:**

*   `annonimized.csv`: Chứa thông tin chi tiết về các lần nộp bài trên WeCode, bao gồm:
    *   `assignment_id`: Mã bài tập
    *   `problem_id`: Mã bài con
    *   Mã số sinh viên (đã ẩn danh)
    *   Thông tin lần nộp có tính điểm hay không
    *   Trạng thái chạy của code
    *   Hệ số nộp bài trễ
    *   Tỷ lệ testcase đúng (làm tròn 2 chữ số và nhân 100)
    *   Thời gian nộp bài
    *   Thời gian chấm bài
    *   Kết quả chấm bài (thời gian và bộ nhớ sử dụng cho mỗi testcase, số lượng testcase sai)
*   Các file dữ liệu kết quả học tập của khoảng 800 sinh viên (`tbtl-public.csv`, `qt-public.csv`, ...), chứa điểm Trung bình tích lũy (TBTL), điểm Quá trình (QT), điểm Thực hành và điểm Cuối kỳ môn IT001.

**Yêu cầu:**

Sinh viên cần xây dựng mô hình dự đoán cho các mục tiêu khác nhau, sử dụng dữ liệu `annonimized.csv` và dữ liệu kết quả học tập đã cung cấp. Cần dự đoán cho **tất cả** mã số sinh viên có trong `annonimized.csv`.

**Tiêu chí đánh giá:**

Các bài nộp sẽ được đánh giá dựa trên **R² score**.

**Lưu ý quan trọng:**

*   Nếu sinh viên có điểm thực tế cho mục tiêu dự đoán nhưng bài nộp không có dự đoán cho sinh viên đó, hệ thống sẽ coi như dự đoán là **0**.

**Các bài tập cụ thể:**

*   **BT1: Dự đoán điểm TBTL sau 1 năm học IT001**
    *   [Link bài tập](https://khmt.uit.edu.vn/wecode/truonganpn/assignment/209/362)
    *   Mục tiêu: Dự đoán điểm Trung bình tích lũy (TBTL) sau 1 năm học cho sinh viên.

*   **BT2: Dự đoán điểm Thực hành IT001**
    *   [Link bài tập](https://khmt.uit.edu.vn/wecode/truonganpn/assignment/209/365)
    *   Mục tiêu: Dự đoán điểm Thực hành môn IT001.

*   **BT3: Dự đoán điểm Quá trình IT001**
    *   [Link bài tập](https://khmt.uit.edu.vn/wecode/truonganpn/assignment/209/364)
    *   Mục tiêu: Dự đoán điểm Quá trình môn IT001.

*   **BT4: Dự đoán điểm Cuối kỳ IT001**
    *   [Link bài tập](https://khmt.uit.edu.vn/wecode/truonganpn/assignment/209/363)
    *   Mục tiêu: Dự đoán điểm Cuối kỳ môn IT001.