fetch("data/data.json")
  .then(function(response) {
    return response.json();
  })
  .then(function(novels) {
    let placeholder = document.querySelector("#data-output");
    let out = "";
    for(let novel of novels) {
      out += `
        <tr>
          <td> <img src='${novel.image}'> </td>

          <td>${novel.title}</td>
          <td>${novel.status}</td>
          <td>${novel.genres}</td>
          <td>${novel.num_volumes}</td>
        </tr>
      `;
    }

    placeholder.innerHTML = out;
  })
