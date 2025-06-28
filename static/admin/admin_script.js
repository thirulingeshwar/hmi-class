function updateStatus(email, status) {
  fetch('/update_status', {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email, status: status })
  }).then(res => res.json())
    .then(data => {
      alert("User status updated!");
      location.reload();
    });
}
