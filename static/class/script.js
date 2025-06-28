document.getElementById("registerForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const phone = document.getElementById("phone").value;
  const email = document.getElementById("email").value;

  fetch("/register", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, phone, email })
  }).then(res => res.json())
    .then(data => {
      document.getElementById("qrcode").style.display = "block";
    });
});
