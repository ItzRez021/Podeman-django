function populateProfile() {
  const name = localStorage.getItem('userName') || '';
  const email = localStorage.getItem('userEmail') || '';
  const avatar = localStorage.getItem('userAvatar');

  document.getElementById('edit-name').value = name;
  document.getElementById('current-email').innerText = email;

  if (avatar) {
    document.getElementById('user-avatar').src = avatar;
  }
}

function saveProfile() {
  localStorage.setItem('userName', document.getElementById('edit-name').value);
  alert('Profile updated successfully.');
}

document.getElementById('upload-avatar').addEventListener('change', function () {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      localStorage.setItem('userAvatar', e.target.result);
      document.getElementById('user-avatar').src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});

populateProfile();
