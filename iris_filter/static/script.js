async function filterData() {
    const species = document.getElementById("species").value;
    const response = await fetch(`/filter-data/${species}`);
    
    if (response.ok) {
        const data = await response.json();
        
        // Populate table with filtered data
        const tableBody = document.querySelector("#data-table tbody");
        tableBody.innerHTML = "";
        
        data.filtered_data.forEach(item => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${item.SepalLengthCm}</td>
                <td>${item.SepalWidthCm}</td>
                <td>${item.PetalLengthCm}</td>
                <td>${item.PetalWidthCm}</td>
                <td>${item.Species}</td>
            `;
            tableBody.appendChild(row);
        });

        // Display the image
        visualization = document.getElementById("visualization");
        visualization.src = `/${data.visualization_image}`;
        visualization.style.display = "block";
    } else {
        alert("Species not found!");
    }
}

