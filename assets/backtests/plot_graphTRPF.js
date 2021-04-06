Plotly.d3.csv("https://raw.githubusercontent.com/jfimbett/AlphaGen.jl/master/csvTRPF.csv?token=AAJ2234V2AI7A5BZZ3FJCZLANLUGS", function(err, rows) {

    function unpack(rows, key) {
        return rows.map(function(row) { return row[key]; });
    }


    var trace1 = {
        type: "scatter",
        mode: "lines",
        name: 'Strategy',
        x: unpack(rows, 'Date'),
        y: unpack(rows, 'Strategy'),
        line: { color: '#168850' }
    }

    var trace2 = {
        type: "scatter",
        mode: "lines",
        name: 'SP500',
        x: unpack(rows, 'Date'),
        y: unpack(rows, 'SP500'),
        line: { color: '#FF5733' }
    }

    var trace3 = {
        type: "scatter",
        mode: "lines",
        name: 'Nasdaq',
        x: unpack(rows, 'Date'),
        y: unpack(rows, 'Nasdaq'),
        line: { color: '#2D1688' }
    }

    var data = [trace1, trace2, trace3];

    var layout = {
        title: 'Growth of Hypothetical $10,000',
    };

    Plotly.newPlot('data-loading', data, layout);
})


Plotly.d3.csv("https://raw.githubusercontent.com/jfimbett/AlphaGen.jl/master/csv_holdingTRPF.csv?token=AAJ223YMOT5PWKWEMZAL3SDANM6TG", function(err, rows) {

    function unpack(rows, key) {
        return rows.map(function(row) { return row[key]; });
    }


    var trace1 = {
        type: "scatter",
        mode: "lines",
        name: 'Positive Returns',
        x: unpack(rows, 'Horizon'),
        y: unpack(rows, 'Beats'),
        line: { color: '#168850' }
    }

    var trace2 = {
        type: "scatter",
        mode: "lines",
        name: 'Beats the Market',
        x: unpack(rows, 'Horizon'),
        y: unpack(rows, 'BeatsM'),
        line: { color: '#FF5733' }
    }



    var data = [trace1, trace2];

    var layout = {
        title: 'Investment Horizons',
        labels: {
            "Horizon": "Horizon (days)",
            "Beats": "% of Time"
        }
    };

    Plotly.newPlot('data-loading2', data, layout);
})