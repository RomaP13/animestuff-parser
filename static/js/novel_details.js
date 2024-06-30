const urlParams = new URLSearchParams(window.location.search);
const novelId = Number(urlParams.get("id"));

fetch("data/data.json")
  .then(response => response.json())
  .then(novels => {
    const novel = novels.find(n => n.id === novelId); // Find the novel by id

    if (novel) {
      document.getElementById("novel-image").src = novel.image;
      document.getElementById("novel-title").textContent = novel.title;
      document.getElementById("novel-synopsis").textContent = novel.synopsis;
      document.getElementById("novel-status").textContent = novel.status;
      document.getElementById("novel-genres").textContent = novel.genres;
      document.getElementById("novel-volumes").textContent = novel.num_volumes;
    } else {
      // Handle the case where the novel is not found
      document.querySelector(".novel-detail-container").innerHTML = "<p>Novel not found.</p>";
    }
  });
