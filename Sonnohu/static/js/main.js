// Đảm bảo code chỉ chạy khi trang đã tải xong
document.addEventListener('DOMContentLoaded', function() {

    // 1. Tự động ẩn các thông báo (Flash messages) sau 5 giây
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // 2. Hiệu ứng cuộn mượt (Smooth Scroll) cho các link nội bộ
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // 3. Thay đổi độ trong suốt của Navbar khi cuộn trang (nếu Sơn muốn)
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('shadow'); // Thêm bóng đổ khi cuộn xuống
        } else {
            navbar.classList.remove('shadow');
        }
    });

    // 4. Kiểm tra mật khẩu khớp nhau ở trang Register (Validate nhanh)
    const regForm = document.querySelector('form[action*="register"]');
    if (regForm) {
        regForm.addEventListener('submit', function(e) {
            const pass = document.getElementById('regPass').value;
            const confirm = document.getElementById('regConfirm').value;
            if (pass !== confirm) {
                e.preventDefault();
                alert("Mật khẩu xác nhận không khớp, Sơn kiểm tra lại nhé!");
            }
        });
    }
});