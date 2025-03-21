document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('like-button').addEventListener('click', function(event) {
        event.preventDefault();
        var novelId = this.getAttribute('data-novel-id');
        fetch(`/like_novel/${novelId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.like_count !== undefined) {
                document.getElementById('like-count').innerText = data.like_count;
                var notification = document.getElementById('notification');
                notification.style.display = 'block';
                setTimeout(function() {
                    notification.style.display = 'none';
                }, 2000);
            }
        });
    });

    document.getElementById('follow-button').addEventListener('click', function(event) {
        event.preventDefault();
        var novelId = this.getAttribute('data-novel-id');
        fetch(`/follow_novel/${novelId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.follow_count !== undefined) {
                document.getElementById('follow-count').innerText = data.follow_count;
                var notification = document.getElementById('notification');
                notification.innerText = data.followed ? 'Followed successfully!' : 'Unfollowed successfully!';
                notification.style.display = 'block';
                setTimeout(function() {
                    notification.style.display = 'none';
                }, 2000);
            }
        });
    });
});