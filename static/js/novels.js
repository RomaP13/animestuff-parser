fetch("data/novels_data.json")
  .then(function(response) {
    return response.json();
  })
  .then(function(novels) {
    let placeholder = document.querySelector("#data-output");
    let out = "";
    for (let novel of novels) {
      out += `
        <tr>
          <td> <img src='${novel.image}'> </td>
          <td><a href='novel_details.html?id=${encodeURIComponent(novel.id)}'>${novel.title}</a></td>
          <td>${novel.status}</td>
          <td>${novel.genres}</td>
          <td>${novel.num_volumes}</td>
        </tr>
      `;
    }

    placeholder.innerHTML = out;
  });
