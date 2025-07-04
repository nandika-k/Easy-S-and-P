//get the DOM elements
const sectorSelect = document.getElementById("sectorFiltering");
const sortSelect = document.getElementById("sorting");
const loadButton = document.getElementById("load");
const tableBody = document.getElementById("stocksTableBody");

function loadStocks() {
    //build url - local for now
    let url = "http://localhost:3306/easy_s_and_p";

    //store parameters relating to stocks to display in this list
    const params = [];
    
    //check for sector filtering and add
    if (sectorSelect) {
        params.push(`sector=${encodeURIComponent(sector)}`);
    }
    //check for sorting and add
    if (sortSelect) {
        params.push(`sort_by=${encodeURIComponent(sort_by)}`);
    }

    //if parameters exist, add to url
    if (params.length > 0) {
        url += "?" + params.join("&");    
    }

    //get the table data and load it
    fetch(url)
    //get HTTP response and check if it's "correct"
    .then(response => {
        //if the response is an error, create an error msg
        if (!response.ok) {
            throw new Error("Failed to get stock data.");
        }
        //else return the data fetched
        return response.json();
    })
    //then, use the response data here to render the table
    .then(data => {
        renderTable(data);
    })
    //if there's an error with getting the data or rendering the table, handle it
    .catch(error => {
        console.error("Error!", error);
        tableBody.innerHTML = "<tr><td>Error loading stocks.<\td><\tr>"
    });
}

function renderTable (stocks) {
    //start table body fresh
    tableBody.innerHTML = ""

    //if no stocks match the criteria, indicate that
    if (stocks.length === 0) {
        tableBody.innerHTML = "<tr><td>No matching stocks.<\td><\tr>"
        return;
    }

    //if there are stocks found, display their data
    stocks.forEach(stock => {
        const row = document.createElement("tr");

        //put relevant information into a row, default to N/A
        row.innerHTML = `
            <td>${stock.Ticker}<\td>
            <td>${stock.Security}<\td>
            <td>${stock.Sector}<\td>
            <td>${stock.Sub_Industry}<\td>
            <td>${stock.Beta ?? "N/A"}<\td>
            <td>${stock.Recommendation_Score ?? "N/A"}<\td>
        `;
        //add row to table
        tableBody.appendChild(row);
    });
}