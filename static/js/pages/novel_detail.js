document.addEventListener("DOMContentLoaded", () => {
    let likeButton = document.getElementById('like-button');
    let listChapter = document.getElementById('idListChapter');
    let addChapterButton = document.getElementById('add-chapter'); // Nút thêm chương

    if (!likeButton || !listChapter) {
        console.error("❌ Không tìm thấy phần tử cần thiết!");
        return;
    }

    let uid = likeButton.getAttribute('data-novel-id');
    if (!uid) {
        console.error("❌ Không lấy được `data-novel-id`!");
        return;
    }

    // 🚀 Lấy danh sách chương
    let fetchChapters = async function() {
        try {
            let response = await fetch(`/apiChapters/?novel=${uid}&ordering=intChapter`);
            console.log("📡 Trạng thái API:", response.status);

            if (!response.ok) {
                throw new Error(`❌ API trả về lỗi ${response.status}`);
            }

            let data = await response.json();
            return data;
        } catch (error) {
            console.error("❌ Lỗi khi gọi API:", error);
            return [];
        }
    };

    // 🚀 Hiển thị danh sách chương
    let updateChapterList = async function() {
        try {
            let data = await fetchChapters();
            if (!Array.isArray(data) || data.length === 0) {
                console.warn("⚠️ Không có dữ liệu chương nào!");
                return;
            }

            listChapter.innerHTML = ''; // Xóa danh sách cũ
            let fragment = document.createDocumentFragment();

            data.forEach((element) => {
                let li = document.createElement('li');
                li.innerHTML = `
                    Chương ${element.intChapter} 
                    <a href='/read_chapter/${element.novel}/${element.intChapter}'>${element.title}</a>
                    <button onclick="deleteChapter(${element.id})">🗑 Xóa</button>
                `;
                fragment.appendChild(li);
            });

            listChapter.appendChild(fragment);
            console.log("✅ Danh sách chương đã cập nhật!");

        } catch (error) {
            console.error("❌ Lỗi trong updateChapterList:", error);
        }
    };

    // 🚀 Thêm chương mới
    let addChapter = async function() {
        let newChapter = {
            novel: uid,
        };

        try {
            let response = await fetch('/apiChapters/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newChapter)
            });

            if (!response.ok) {
                throw new Error("❌ Lỗi khi thêm chương mới!");
            }

            console.log("✅ Chương mới đã được thêm!");
            updateChapterList(); // Cập nhật danh sách sau khi thêm

        } catch (error) {
            console.error("❌ Lỗi trong addChapter:", error);
        }
    };

    // 🚀 Xóa chương
    window.deleteChapter = async function(chapterId) {
        if (!confirm("Bạn có chắc chắn muốn xóa chương này?")) return;

        try {
            let response = await fetch(`/apiChapters/${chapterId}/`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error("❌ Lỗi khi xóa chương!");
            }

            console.log("✅ Chương đã được xóa!");
            updateChapterList(); // Cập nhật danh sách sau khi xóa

        } catch (error) {
            console.error("❌ Lỗi trong deleteChapter:", error);
        }
    };

    // 🚀 Cập nhật danh sách khi trang tải
    updateChapterList();

    // 🎯 Sự kiện thêm chương
    if (addChapterButton) {
        addChapterButton.addEventListener("click", addChapter);
    }
});

