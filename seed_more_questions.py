import json
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Question, QuestionType

DATABASE_URL = "sqlite:///./learning_app.db"
engine = create_engine(DATABASE_URL, echo=False)

new_questions = [
    # === TOPIC 101: Python cơ bản (Thêm 10 câu) ===
    {
        "topic_id": 101,
        "content": "[Python] Trong Python, kết quả của biểu thức `[x**2 for x in range(5) if x % 2 == 0]` là gì?",
        "options": {"A": "[0, 4, 16]", "B": "[0, 1, 4, 9, 16]", "C": "[4, 16]", "D": "[0, 2, 4]"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "range(5) sinh ra [0, 1, 2, 3, 4]. Các số chẵn là 0, 2, 4. Bình phương tương ứng là 0, 4, 16."
    },
    {
        "topic_id": 101,
        "content": "[Python] Kiểu dữ liệu nào sau đây trong Python là Mutable (có thể thay đổi nội dung sau khi tạo)?",
        "options": {"A": "List và Dictionary", "B": "Tuple và String", "C": "Frozenset và Int", "D": "Float và Boolean"},
        "correct": "A", "difficulty": 1.5,
        "explanation": "List, Dict, Set là mutable. Trong khi Tuple, String, Int, Float là immutable."
    },
    {
        "topic_id": 101,
        "content": "[Python] Sự khác biệt chính giữa toán tử `is` và `==` trong Python là gì?",
        "options": {"A": "`is` so sánh định danh vùng nhớ (id), còn `==` so sánh giá trị nội dung", "B": "`==` so sánh id vùng nhớ, còn `is` so sánh giá trị", "C": "Cả hai toán tử hoàn toàn tương đương nhau", "D": "`is` chỉ dùng cho số nguyên"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "`==` kiểm tra giá trị của 2 đối tượng, còn `is` kiểm tra xem 2 biến có cùng trỏ tới cùng một ô nhớ hay không."
    },
    {
        "topic_id": 101,
        "content": "[Python] Generator trong Python khác hàm thông thường ở điểm nào?",
        "options": {"A": "Dùng từ khóa `yield` thay vì `return` để trả về từng giá trị theo cơ chế lazy evaluation (tiết kiệm RAM)", "B": "Tạo ra một danh sách đầy đủ lưu sẵn trong RAM", "C": "Chạy nhanh gấp 10 lần nhưng tốn RAM hơn", "D": "Chỉ chạy được trên môi trường Linux"},
        "correct": "A", "difficulty": 3.0,
        "explanation": "Generator sinh giá trị theo yêu cầu (lazy evaluation) bằng yield, không tải toàn bộ dữ liệu vào bộ nhớ cùng lúc."
    },
    {
        "topic_id": 101,
        "content": "[Python] Phương thức `dict.get(key, default)` có ưu điểm gì so với cách truy cập `dict[key]` thông thường?",
        "options": {"A": "Không ném ngoại lệ KeyError nếu key không tồn tại, mà trả về giá trị mặc định", "B": "Tự động xóa key sau khi đọc", "C": "Tăng tốc độ truy xuất lên 50%", "D": "Khóa từ điển để tránh ghi đè"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "Truy cập dict[key] với key không có sẽ gây lỗi KeyError. Dùng dict.get(key, default) an toàn hơn."
    },
    {
        "topic_id": 101,
        "content": "[Python] Khi định nghĩa hàm `def func(*args, **kwargs):`, tham số `*args` và `**kwargs` lần lượt nhận kiểu dữ liệu gì?",
        "options": {"A": "`args` nhận Tuple các tham số vị trí, `kwargs` nhận Dict các tham số đặt tên", "B": "`args` nhận List, `kwargs` nhận Tuple", "C": "Cả hai đều nhận Set", "D": "`args` nhận Dict, `kwargs` nhận List"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "`*args` gom các positional arguments thành Tuple, `**kwargs` gom các keyword arguments thành Dictionary."
    },
    {
        "topic_id": 101,
        "content": "[Python] Câu lệnh `with open('data.txt', 'r') as f:` (Context Manager) mang lại lợi ích cốt lõi nào?",
        "options": {"A": "Đảm bảo file luôn được đóng an toàn kể cả khi có ngoại lệ Exception phát sinh", "B": "Tự động dịch nội dung file sang tiếng Việt", "C": "Tăng tốc độ đọc file bằng đa luồng", "D": "Nén dung lượng file tự động"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "Context manager tự động gọi __exit__ để close() tài nguyên, tránh rò rỉ file handle."
    },
    {
        "topic_id": 101,
        "content": "[Python] Kết quả của biểu thức `sorted([3, 1, 4, 1, 5], reverse=True)` là gì?",
        "options": {"A": "[5, 4, 3, 1, 1]", "B": "[1, 1, 3, 4, 5]", "C": "[5, 4, 3, 1]", "D": "[3, 1, 4, 1, 5]"},
        "correct": "A", "difficulty": 1.5,
        "explanation": "`reverse=True` sắp xếp danh sách theo thứ tự giảm dần và giữ nguyên các phần tử trùng lặp."
    },
    {
        "topic_id": 101,
        "content": "[Python] Trong lập trình Hướng đối tượng Python, phương thức `__init__` đóng vai trò gì?",
        "options": {"A": "Hàm khởi tạo (constructor) dùng để gán giá trị thuộc tính ban đầu cho đối tượng", "B": "Hàm hủy (destructor) giải phóng bộ nhớ", "C": "Hàm kiểm tra cú pháp của Class", "D": "Hàm chuyển đổi Class thành chuỗi"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "`__init__` là phương thức đặc biệt được tự động gọi khi khởi tạo một instance mới từ class."
    },
    {
        "topic_id": 101,
        "content": "[Python] Thư viện tích hợp sẵn nào trong Python thường được sử dụng để sao chép sâu (deep copy) một đối tượng lồng nhau?",
        "options": {"A": "`copy.deepcopy()`", "B": "`clone.make()`", "C": "`os.duplicate()`", "D": "`sys.deepcopy()`"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "Module `copy` cung cấp `copy.copy()` (shallow copy) và `copy.deepcopy()` (sao chép độc lập toàn bộ đối tượng lồng bên trong)."
    },

    # === TOPIC 102: NumPy & Xử lý Ma trận (Thêm 10 câu) ===
    {
        "topic_id": 102,
        "content": "[NumPy] Quy tắc phát sóng (Broadcasting) trong NumPy cho phép điều gì?",
        "options": {"A": "Thực hiện các phép toán số học giữa các mảng có kích thước (shapes) khác nhau mà không cần sao chép dữ liệu dư thừa", "B": "Phát trực tiếp dữ liệu qua mạng Wifi", "C": "Chuyển đổi kiểu dữ liệu int sang chuỗi", "D": "Nén mảng thành file zip"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "Broadcasting tự động duỗi ảo kích thước các chiều có độ dài bằng 1 hoặc chiều bị thiếu để tương thích kích thước khi tính toán."
    },
    {
        "topic_id": 102,
        "content": "[NumPy] Cho mảng `a = np.array([[1, 2, 3], [4, 5, 6]])`. Kích thước `a.shape` và số chiều `a.ndim` lần lượt là:",
        "options": {"A": "shape: (2, 3), ndim: 2", "B": "shape: (3, 2), ndim: 2", "C": "shape: (6,), ndim: 1", "D": "shape: (2, 3), ndim: 6"},
        "correct": "A", "difficulty": 1.5,
        "explanation": "Mảng có 2 hàng và 3 cột nên shape là (2, 3), số chiều không gian (ndim) là 2."
    },
    {
        "topic_id": 102,
        "content": "[NumPy] Phép toán `np.dot(A, B)` hoặc toán tử `A @ B` đại diện cho phép tính nào?",
        "options": {"A": "Phép nhân ma trận (Matrix Multiplication)", "B": "Nhân từng phần tử tương ứng (Hadamard product)", "C": "Cộng hai ma trận", "D": "Chia từng phần tử tương ứng"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "`A @ B` hoặc `np.dot(A, B)` là phép nhân ma trận chuẩn đại số tuyến tính, khác với `A * B` là nhân từng phần tử."
    },
    {
        "topic_id": 102,
        "content": "[NumPy] Lệnh nào sau đây dùng để tính ma trận nghịch đảo của ma trận vuông A trong NumPy?",
        "options": {"A": "`np.linalg.inv(A)`", "B": "`np.inverse(A)`", "C": "`np.matrix.rev(A)`", "D": "`A.T`"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "Module `np.linalg` chứa các hàm đại số tuyến tính nâng cao, trong đó `np.linalg.inv()` tính ma trận nghịch đảo."
    },
    {
        "topic_id": 102,
        "content": "[NumPy] Để gộp (ghép nối) hai mảng theo chiều dọc (theo hàng), ta dùng hàm nào?",
        "options": {"A": "`np.vstack([A, B])` hoặc `np.concatenate([A, B], axis=0)`", "B": "`np.hstack([A, B])`", "C": "`np.append_cols(A, B)`", "D": "`np.merge(A, B)`"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "vstack (vertical stack) ghép theo hàng dọc (axis=0), trong khi hstack ghép theo cột ngang (axis=1)."
    },
    {
        "topic_id": 102,
        "content": "[NumPy] Kỹ thuật Boolean Masking `arr[arr > 5]` trả về kết quả gì?",
        "options": {"A": "Một mảng 1D chỉ chứa các phần tử của arr có giá trị lớn hơn 5", "B": "Mảng các giá trị True/False", "C": "Một số nguyên duy nhất", "D": "Lỗi cú pháp"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "Truyền điều kiện logic vào ngoặc vuông mảng sẽ lọc ra chính xác các phần tử thỏa mãn điều kiện đó."
    },
    {
        "topic_id": 102,
        "content": "[NumPy] Hàm `np.argmax(arr, axis=1)` có chức năng gì?",
        "options": {"A": "Tìm chỉ số (index) của phần tử có giá trị lớn nhất trên từng hàng", "B": "Tìm giá trị lớn nhất trong toàn bộ mảng", "C": "Đếm số phần tử dương", "D": "Sắp xếp mảng theo thứ tự tăng dần"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "`np.argmax` trả về vị trí index của giá trị cực đại. `axis=1` chỉ định quét theo từng hàng."
    },
    {
        "topic_id": 102,
        "content": "[NumPy] Hàm `np.linspace(0, 1, 5)` trả về mảng nào sau đây?",
        "options": {"A": "array([0.  , 0.25, 0.5 , 0.75, 1.  ])", "B": "array([0, 1, 2, 3, 4])", "C": "array([0.1, 0.2, 0.3, 0.4, 0.5])", "D": "array([0, 1])"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "`np.linspace(start, stop, num)` tạo ra `num` điểm cách đều nhau trong đoạn [start, stop] (bao gồm cả điểm cuối)."
    },
    {
        "topic_id": 102,
        "content": "[NumPy] Ma trận chuyển vị (Transpose) của mảng `A` được gọi bằng cú pháp nào?",
        "options": {"A": "`A.T` hoặc `np.transpose(A)`", "B": "`A.reverse()`", "C": "`A.flip()`", "D": "`np.inv(A)`"},
        "correct": "A", "difficulty": 1.5,
        "explanation": "Thuộc tính `.T` đổi hàng thành cột và cột thành hàng của ma trận."
    },
    {
        "topic_id": 102,
        "content": "[NumPy] Vì sao các phép toán trên mảng NumPy chạy nhanh hơn hàng chục lần so với vòng lặp List Python thuần?",
        "options": {"A": "Vì NumPy lưu dữ liệu liên tục trong bộ nhớ C (contiguous memory) và hỗ trợ tính toán vector hóa (Vectorization)", "B": "Vì NumPy chạy trên card đồ họa mặc định", "C": "Vì NumPy tự động bỏ qua các số lẻ", "D": "Vì NumPy nén dữ liệu dạng nhị phân"},
        "correct": "A", "difficulty": 3.0,
        "explanation": "Vectorization trong C tận dụng tập lệnh CPU SIMD và bộ nhớ liền kề, loại bỏ hoàn toàn overhead của thông dịch viên Python."
    },

    # === TOPIC 103: Pandas & Xử lý Dữ liệu (Thêm 10 câu) ===
    {
        "topic_id": 103,
        "content": "[Pandas] Sự khác biệt cơ bản giữa `df.loc[]` và `df.iloc[]` là gì?",
        "options": {"A": "`df.loc` truy cập theo Nhãn (label-based), còn `df.iloc` truy cập theo Vị trí số nguyên (integer index-based)", "B": "`df.iloc` truy cập theo nhãn, `df.loc` theo vị trí", "C": "Hai phương thức giống hệt nhau", "D": "`df.loc` chỉ dùng cho cột, `df.iloc` chỉ dùng cho hàng"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "loc lọc theo tên cột và nhãn hàng (index name), iloc lọc theo chỉ số vị trí 0, 1, 2... (integer position)."
    },
    {
        "topic_id": 103,
        "content": "[Pandas] Lệnh nào sau đây dùng để xử lý dữ liệu khuyết thiếu (NaN) bằng cách thay thế chúng bằng giá trị trung bình của cột 'age'?",
        "options": {"A": "`df['age'].fillna(df['age'].mean(), inplace=True)`", "B": "`df['age'].dropna()`", "C": "`df['age'].replace_null()`", "D": "`df['age'].set_mean()`"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "`fillna()` là phương thức điền dữ liệu khuyết thiếu, truyền `df['age'].mean()` để điền giá trị trung bình."
    },
    {
        "topic_id": 103,
        "content": "[Pandas] Để xóa hoàn toàn các hàng có chứa ít nhất một ô dữ liệu bị thiếu (NaN), ta dùng lệnh nào?",
        "options": {"A": "`df.dropna(axis=0)`", "B": "`df.drop_nulls()`", "C": "`df.delete_empty()`", "D": "`df.clean()`"},
        "correct": "A", "difficulty": 1.5,
        "explanation": "`df.dropna()` với mặc định `axis=0` sẽ loại bỏ toàn bộ các hàng có giá trị rỗng/khuyết thiếu."
    },
    {
        "topic_id": 103,
        "content": "[Pandas] Cú pháp nào dùng để tính giá trị trung bình doanh số ('sales') phân nhóm theo từng phòng ban ('department')?",
        "options": {"A": "`df.groupby('department')['sales'].mean()`", "B": "`df.group('department').sales.avg()`", "C": "`df.filter('department').mean()`", "D": "`df.aggregate('sales').by('department')`"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "Mô hình Split-Apply-Combine trong Pandas được thực hiện qua `df.groupby('cột_gom_nhóm')['cột_tính_toán'].hàm_thống_kê()`."
    },
    {
        "topic_id": 103,
        "content": "[Pandas] Để gộp hai bảng DataFrame `df1` và `df2` dựa trên khóa chung `customer_id` tương tự phép INNER JOIN trong SQL, ta dùng hàm nào?",
        "options": {"A": "`pd.merge(df1, df2, on='customer_id', how='inner')`", "B": "`pd.concat([df1, df2])`", "C": "`df1.append(df2)`", "D": "`pd.combine(df1, df2)`"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "`pd.merge` là hàm ghép nối hai DataFrame chuẩn SQL với các tùy chọn inner, outer, left, right."
    },
    {
        "topic_id": 103,
        "content": "[Pandas] Lệnh `df['column'].value_counts()` có tác dụng gì?",
        "options": {"A": "Đếm tần suất xuất hiện của từng giá trị phân loại riêng biệt trong cột", "B": "Tính tổng các giá trị số trong cột", "C": "Tìm giá trị lớn nhất trong cột", "D": "Kiểm tra kiểu dữ liệu của cột"},
        "correct": "A", "difficulty": 1.5,
        "explanation": "`value_counts()` đếm số lần xuất hiện của mỗi giá trị độc nhất trong Series và sắp xếp giảm dần."
    },
    {
        "topic_id": 103,
        "content": "[Pandas] Phương thức `df.apply(lambda x: ...)` dùng để làm gì?",
        "options": {"A": "Áp dụng một hàm tính toán tùy biến lên từng phần tử, từng hàng hoặc từng cột của DataFrame", "B": "Tự động cài đặt thư viện mới", "C": "Đổi tên cột của bảng", "D": "Xuất dữ liệu ra file Excel"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "`apply()` giúp tùy biến biến đổi dữ liệu hàng loạt linh hoạt theo hàm tự định nghĩa."
    },
    {
        "topic_id": 103,
        "content": "[Pandas] Hàm `df.describe()` hiển thị các chỉ số thống kê mô tả nào đối với các cột dạng số?",
        "options": {"A": "Count, Mean, Std, Min, 25%, 50% (Median), 75%, Max", "B": "Chỉ hiển thị tên tác giả và ngày tạo bảng", "C": "Danh sách các lỗi chính tả", "D": "Tốc độ xử lý của RAM"},
        "correct": "A", "difficulty": 1.5,
        "explanation": "`describe()` tóm tắt nhanh phân phối của dữ liệu dạng số với 8 chỉ số thống kê cơ bản."
    },
    {
        "topic_id": 103,
        "content": "[Pandas] Khi muốn chuyển đổi một cột chuỗi chứa ngày tháng sang định dạng chuẩn datetime, ta sử dụng hàm nào?",
        "options": {"A": "`pd.to_datetime(df['date_column'])`", "B": "`df['date_column'].as_date()`", "C": "`pd.format_time(df['date_column'])`", "D": "`df['date_column'].convert_time()`"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "`pd.to_datetime()` chuyển đổi chuỗi ngày tháng sang định dạng DatetimeIndex hoặc Series kiểu datetime64."
    },
    {
        "topic_id": 103,
        "content": "[Pandas] Để loại bỏ hoàn toàn các dòng bị trùng lặp (duplicate rows) trong DataFrame, phương thức nào được sử dụng?",
        "options": {"A": "`df.drop_duplicates()`", "B": "`df.unique()`", "C": "`df.remove_same()`", "D": "`df.distinct()`"},
        "correct": "A", "difficulty": 1.5,
        "explanation": "`drop_duplicates()` loại bỏ các bản ghi trùng lặp và giữ lại bản ghi đầu tiên theo mặc định."
    },

    # === TOPIC 104: Tối ưu hóa & Gradient Descent (Thêm 10 câu) ===
    {
        "topic_id": 104,
        "content": "[Gradient Descent] Trong bài toán hồi quy tuyến tính, hàm mất mát thường dùng là Mean Squared Error (MSE). Vì sao hàm này là hàm lồi (Convex Function)?",
        "options": {"A": "Vì đạo hàm bậc hai (Ma trận Hessian) là bán xác định dương, đảm bảo chỉ có duy nhất một điểm cực tiểu toàn cục", "B": "Vì nó có nhiều điểm cực tiểu cục bộ", "C": "Vì giá trị của nó luôn luôn âm", "D": "Vì đồ thị của nó là đường thẳng"},
        "correct": "A", "difficulty": 3.5,
        "explanation": "Hàm lồi có tính chất đặc biệt là mọi điểm cực tiểu cục bộ đều là điểm cực tiểu toàn cục (Global Minimum), giúp Gradient Descent không bị bẫy."
    },
    {
        "topic_id": 104,
        "content": "[Gradient Descent] Thuật toán Mini-batch Gradient Descent dung hòa ưu điểm của Batch GD và Stochastic GD (SGD) như thế nào?",
        "options": {"A": "Cập nhật trọng số trên từng nhóm nhỏ (batch size vd 32, 64) vừa tận dụng được tăng tốc phần cứng GPU vừa đảm bảo hướng hội tụ ổn định", "B": "Chỉ dùng 1 mẫu dữ liệu duy nhất", "C": "Dùng toàn bộ dữ liệu trên RAM", "D": "Không cần tính đạo hàm"},
        "correct": "A", "difficulty": 3.0,
        "explanation": "Mini-batch cân bằng giữa tốc độ tính toán song song ma trận trên phần cứng và giảm dao động ngẫu nhiên so với SGD thuần."
    },
    {
        "topic_id": 104,
        "content": "[Gradient Descent] Thuật toán Adam Optimizer (Adaptive Moment Estimation) kết hợp hai cơ chế tiên tiến nào?",
        "options": {"A": "Momentum (ước lượng moment bậc 1) và RMSProp (ước lượng moment bậc 2 không định tâm)", "B": "L1 và L2 Regularization", "C": "Decision Tree và Random Forest", "D": "KNN và Naive Bayes"},
        "correct": "A", "difficulty": 4.0,
        "explanation": "Adam kết hợp ưu điểm của Momentum (lướt nhanh qua vùng dốc) và RMSProp (điều chỉnh tốc độ học thích ứng cho từng tham số)."
    },
    {
        "topic_id": 104,
        "content": "[Gradient Descent] Hiện tượng Bùng nổ Gradient (Exploding Gradient) là gì và kỹ thuật nào thường dùng để kiểm soát nó?",
        "options": {"A": "Gradient tăng quá lớn làm trọng số tràn số (NaN); giải quyết bằng Kẹp Gradient (Gradient Clipping)", "B": "Gradient giảm về 0; giải quyết bằng tăng Epochs", "C": "Mô hình học quá nhanh; giải quyết bằng xóa bớt dữ liệu", "D": "Mất dữ liệu bộ nhớ Cache"},
        "correct": "A", "difficulty": 3.5,
        "explanation": "Exploding Gradient khiến trọng số nhảy vọt ra vô cùng. Kỹ thuật Gradient Clipping giới hạn độ dài vector đạo hàm không vượt quá một ngưỡng c."
    },
    {
        "topic_id": 104,
        "content": "[Gradient Descent] Trong công thức cập nhật trọng số `w = w - alpha * dJ/dw`, dấu trừ mang ý nghĩa hình học gì?",
        "options": {"A": "Di chuyển ngược hướng với vector Gradient để đi về phía giá trị hàm mất mát giảm dần", "B": "Tăng giá trị hàm mất mát lên cực đại", "C": "Đổi dấu kết quả dự đoán", "D": "Chỉ là quy ước ký hiệu không có ý nghĩa toán học"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "Vector Gradient luôn chỉ hướng dốc tăng nhanh nhất. Để tìm cực tiểu (giảm hàm mất mát), ta phải đi ngược chiều vector gradient (dấu trừ)."
    },
    {
        "topic_id": 104,
        "content": "[Gradient Descent] Điểm yên ngựa (Saddle Point) trong không gian nhiều chiều có đặc điểm gì gây khó khăn cho việc tối ưu hóa?",
        "options": {"A": "Đạo hàm bậc nhất bằng 0 nhưng là cực đại theo chiều này và cực tiểu theo chiều khác, làm thuật toán dễ bị kẹt", "B": "Đạo hàm bằng vô cùng", "C": "Không thể tính được giá trị", "D": "Là điểm tối ưu toàn cục duy nhất"},
        "correct": "A", "difficulty": 3.5,
        "explanation": "Tại Saddle Point, gradient xấp xỉ 0 khiến các thuật toán bậc 1 chuyển động cực kỳ chậm hoặc đứng yên nếu không có momentum."
    },
    {
        "topic_id": 104,
        "content": "[Gradient Descent] Chiến lược Giảm dần Tốc độ học (Learning Rate Decay / Scheduling) có mục đích gì?",
        "options": {"A": "Bắt đầu với bước nhảy lớn để tiếp cận vùng tối ưu nhanh, sau đó thu nhỏ bước nhảy để hội tụ mượt mà vào đáy", "B": "Tăng dần tốc độ học khi gần đến đích", "C": "Giữ nguyên learning rate không đổi", "D": "Làm mô hình chạy vô hạn"},
        "correct": "A", "difficulty": 3.0,
        "explanation": "Learning rate scheduling giúp tránh việc bước nhảy quá lớn nhảy qua nhảy lại quanh điểm cực tiểu ở giai đoạn cuối quá trình huấn luyện."
    },
    {
        "topic_id": 104,
        "content": "[Gradient Descent] Đạo hàm riêng của hàm mất mát MSE `J(w) = (1/2m) * sum((y_pred - y)^2)` theo trọng số `w_j` có dạng là:",
        "options": {"A": "`dJ/dw_j = (1/m) * sum((y_pred - y) * x_j)`", "B": "`dJ/dw_j = sum(y_pred - y)`", "C": "`dJ/dw_j = (1/m) * sum(x_j^2)`", "D": "`dJ/dw_j = 2 * (y_pred - y)`"},
        "correct": "A", "difficulty": 3.0,
        "explanation": "Theo quy tắc dây chuyền (chain rule), đạo hàm của (y_pred - y)^2 nhân đạo hàm bên trong theo w_j (chính là x_j), hệ số 2 triệt tiêu 1/2."
    },
    {
        "topic_id": 104,
        "content": "[Gradient Descent] Vì sao việc Khởi tạo Trọng số ngẫu nhiên (Random Initialization) lại tối quan trọng thay vì gán toàn bộ trọng số bằng 0 trong Mạng nơ-ron?",
        "options": {"A": "Để phá vỡ tính đối xứng (Break Symmetry), tránh việc tất cả các nơ-ron học các đặc trưng giống hệt nhau", "B": "Để giảm dung lượng lưu trữ trên đĩa", "C": "Để tránh lỗi chia cho 0", "D": "Chỉ để làm code đẹp hơn"},
        "correct": "A", "difficulty": 3.5,
        "explanation": "Nếu khởi tạo toàn bộ trọng số bằng 0, mọi nơ-ron ở cùng một lớp ẩn sẽ có cùng đạo hàm và cập nhật hệt nhau qua mọi epoch."
    },
    {
        "topic_id": 104,
        "content": "[Gradient Descent] Thuật toán Lan truyền ngược (Backpropagation) thực chất là sự ứng dụng của quy tắc toán học nào?",
        "options": {"A": "Quy tắc dây chuyền (Chain Rule) trong giải tích vi phân", "B": "Định lý Pytago", "C": "Quy tắc Cramer giải hệ phương trình", "D": "Định lý Bayes trong xác suất"},
        "correct": "A", "difficulty": 3.0,
        "explanation": "Backpropagation tính đạo hàm riêng của hàm mất mát theo từng trọng số ở các lớp sâu bằng cách áp dụng quy tắc dây chuyền từ lớp ra về lớp vào."
    },

    # === TOPIC 105: Học máy Scikit-Learn (Thêm 10 câu) ===
    {
        "topic_id": 105,
        "content": "[Scikit-Learn] Hàm `train_test_split(X, y, test_size=0.2, random_state=42)` có tham số `random_state` đóng vai trò gì?",
        "options": {"A": "Thiết lập seed ngẫu nhiên để việc chia tập dữ liệu có thể tái lập kết quả giống hệt nhau ở các lần chạy sau", "B": "Tự động tăng số lượng mẫu kiểm thử lên gấp đôi", "C": "Xáo trộn nhãn ngẫu nhiên", "D": "Chọn số luồng CPU"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "`random_state` cố định pseudo-random number generator, giúp đồng nghiệp hoặc lần chạy sau chia tập train/test hoàn toàn nhất quán."
    },
    {
        "topic_id": 105,
        "content": "[Scikit-Learn] Chỉ số F1-Score là trung bình điều hòa (Harmonic Mean) của hai thước đo nào?",
        "options": {"A": "Precision (Độ chuẩn xác) và Recall (Độ thu hồi)", "B": "Accuracy và Loss", "C": "Bias và Variance", "D": "True Positive và False Positive"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "F1-Score = 2 * (Precision * Recall) / (Precision + Recall), đặc biệt hữu ích khi đánh giá tập dữ liệu mất cân bằng nhãn (imbalanced data)."
    },
    {
        "topic_id": 105,
        "content": "[Scikit-Learn] Trong bài toán chẩn đoán ung thư, ta quan tâm nhất đến việc không bỏ sót bất kỳ ca bệnh nào (giảm False Negative về tối thiểu). Ta nên ưu tiên tối ưu hóa chỉ số nào?",
        "options": {"A": "Recall (Độ thu hồi / Độ nhạy Sensitivity)", "B": "Precision", "C": "Accuracy", "D": "Specificity"},
        "correct": "A", "difficulty": 3.0,
        "explanation": "Recall = TP / (TP + FN). Khi FN (bệnh nhân có bệnh nhưng bị đoán là khỏe) thấp thì Recall sẽ cao, tránh bỏ sót người bệnh."
    },
    {
        "topic_id": 105,
        "content": "[Scikit-Learn] Kỹ thuật Regularization L1 (Lasso) khác L2 (Ridge) ở điểm đặc trưng nào?",
        "options": {"A": "L1 có khả năng ép các hệ số trọng số không quan trọng về đúng bằng 0 (Feature Selection tự động)", "B": "L2 ép trọng số về đúng bằng 0, còn L1 chỉ thu nhỏ", "C": "L1 chỉ dùng cho phân loại, L2 chỉ dùng cho hồi quy", "D": "Cả hai phương pháp giống hệt nhau"},
        "correct": "A", "difficulty": 3.5,
        "explanation": "Lasso cộng thêm trị tuyệt đối |w| vào loss, tạo ra tính chất thưa (sparsity) và tự động triệt tiêu các đặc trưng dư thừa về 0."
    },
    {
        "topic_id": 105,
        "content": "[Scikit-Learn] Hiện tượng Quá khớp (Overfitting) được biểu hiện như thế nào khi quan sát hiệu năng của mô hình?",
        "options": {"A": "Điểm trên tập Huấn luyện (Training set) cực cao nhưng điểm trên tập Kiểm thử (Test/Val set) rất thấp", "B": "Điểm trên cả 2 tập đều rất thấp", "C": "Điểm trên tập Test cao hơn tập Train", "D": "Mô hình không hội tụ"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "Overfitting xảy ra khi mô hình học thuộc lòng cả nhiễu của tập Train, dẫn đến khả năng tổng quát hóa (generalization) kém trên dữ liệu mới."
    },
    {
        "topic_id": 105,
        "content": "[Scikit-Learn] Thuật toán Rừng Ngẫu nhiên (Random Forest) áp dụng kỹ thuật kết hợp mô hình nào?",
        "options": {"A": "Bagging (Bootstrap Aggregating) kết hợp chọn tập con đặc trưng ngẫu nhiên", "B": "Boosting tuần tự", "C": "Stacking với mạng nơ-ron", "D": "Voting mềm các mô hình tuyến tính"},
        "correct": "A", "difficulty": 3.0,
        "explanation": "Random Forest xây dựng nhiều cây quyết định độc lập trên các mẫu bootstrap dữ liệu và lấy trung bình hoặc bầu chọn số đông để giảm phương sai (variance)."
    },
    {
        "topic_id": 105,
        "content": "[Scikit-Learn] Công cụ `StandardScaler` trong `sklearn.preprocessing` biến đổi dữ liệu theo công thức chuẩn hóa nào?",
        "options": {"A": "`z = (x - mean) / std` (đưa về phân phối có trung bình 0 và độ lệch chuẩn 1)", "B": "`z = (x - min) / (max - min)` (đưa về đoạn [0, 1])", "C": "`z = log(x)`", "D": "`z = x^2`"},
        "correct": "A", "difficulty": 2.0,
        "explanation": "StandardScaler trừ giá trị trung bình rồi chia độ lệch chuẩn (Z-score normalization). Min-Max Scaler mới đưa về [0, 1]."
    },
    {
        "topic_id": 105,
        "content": "[Scikit-Learn] Công cụ `GridSearchCV` trong Scikit-Learn dùng để làm gì?",
        "options": {"A": "Tìm kiếm tổ hợp siêu tham số (Hyperparameters) tối ưu thông qua kỹ thuật kiểm định chéo (Cross-Validation)", "B": "Tìm kiếm hình ảnh trên Google", "C": "Vẽ biểu đồ lưới phân bố dữ liệu", "D": "Nén mô hình để chạy trên điện thoại"},
        "correct": "A", "difficulty": 2.5,
        "explanation": "GridSearchCV duyệt qua toàn bộ lưới các giá trị tham số được chỉ định, huấn luyện và đánh giá để tìm ra bộ cấu hình tốt nhất."
    },
    {
        "topic_id": 105,
        "content": "[Scikit-Learn] Khi huấn luyện một mô hình trong Scikit-Learn, quy trình chuẩn mực thông qua 3 phương thức cốt lõi là gì?",
        "options": {"A": "Khởi tạo mô hình -> `.fit(X_train, y_train)` -> `.predict(X_test)`", "B": "Khởi tạo -> `.run()` -> `.export()`", "C": "Khởi tạo -> `.compile()` -> `.train()`", "D": "Khởi tạo -> `.start()` -> `.stop()`"},
        "correct": "A", "difficulty": 1.5,
        "explanation": "API của Scikit-Learn được thiết kế nhất quán: Khởi tạo Estimator, gọi fit() để học từ dữ liệu, và gọi predict() để suy luận."
    },
    {
        "topic_id": 105,
        "content": "[Scikit-Learn] Đường cong ROC-AUC đánh giá chất lượng của mô hình phân loại nhị phân. Giá trị AUC = 0.5 thể hiện điều gì?",
        "options": {"A": "Mô hình dự đoán hoàn toàn ngẫu nhiên (không tốt hơn việc tung đồng xu)", "B": "Mô hình hoàn hảo tuyệt đối", "C": "Mô hình dự đoán sai 100%", "D": "Mô hình bị lỗi thuật toán"},
        "correct": "A", "difficulty": 3.0,
        "explanation": "AUC = 1.0 là mô hình phân loại hoàn hảo. AUC = 0.5 tương đương với việc đoán mò ngẫu nhiên (random guess)."
    }
]

with Session(engine) as session:
    added_count = 0
    for q_data in new_questions:
        q = Question(
            topic_id=q_data["topic_id"],
            content=q_data["content"],
            question_type=QuestionType.MULTIPLE_CHOICE,
            options=q_data["options"],
            correct_answer=q_data["correct"],
            explanation=q_data["explanation"],
            difficulty_level=q_data["difficulty"]
        )
        session.add(q)
        added_count += 1
    session.commit()
    print(f"SUCCESS: Đã nạp thành công {added_count} câu hỏi chất lượng cao mới vào CSDL!")
