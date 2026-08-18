/** All function for the game with engine */

/*
Create the chart system for the game
*/
const chart_data = [{"move": 0, "value": 50},]

const game_chart_config = {
    type: "line", data: {
        labels: chart_data.map(row => row.move), datasets: [{
            data: chart_data.map(row => row.value),
            pointRadius: 0,
            fill: true,
            cubicInterpolationMode: 'monotone',
            borderColor: "#00000000",
            backgroundColor: "rgba(0,0,0,0.52)",
        }]
    }, yAxes: [{
        display: true, ticks: {
            beginAtZero: true, steps: 10, stepValue: 5, max: 100, min: 0,
        },

    }], options: {
        responsive: true, maintainAspectRatio: false,

        y: {suggestedMin: 0, suggestedMax: 100}, animation: {duration: 0}, scales: {
            x: {
                grid: {drawOnChartArea: false}, ticks: {color: "#000000"}
            }, y: {
                grid: {drawOnChartArea: false}, ticks: {color: "#000000"}
            },

        }, scaleFontColor: "#000000", // hide dataset label
        plugins: {
            legend: {
                position: 'top', display: false,
            }, title: {
                display: false, text: 'Chart.js Line Chart',
            },
        },
    }
}

const game_old = new Chart(document.getElementById('score_chart'), game_chart_config)

let advice = true;

/*
All function for the game
*/
function plot_board(board, player) {
    /**
     This function plot the board depending on the board given in param
     this script only support 8*8 game
     @param board - a 2d array that contain board information
     */
    let board_string = "";

    for (let y = 0; y < 8; y++) {
        // start a new line in the board
        board_string += '<div class="board_line">'

        for (let x = 0; x < 8; x++) {
            // start a new row in the line
            board_string += '<div class="board_case">'

            // for black pieces
            if (board[y][x] === PIECE_BLACK) {
                board_string += '<div class="black_piece"></div>'

            }
            // for white pieces
            else if (board[y][x] === PIECE_WHITE) {
                board_string += '<div class="white_piece"></div>'

            }
            // for possible moves
            else if (board[y][x] === PIECE_MOVE) {
                if (!advice) {
                    board_string += `<div class="possible_move_none" id="${x}_${y}" onclick="play(${x},${y})"></div>`
                } else if (player === PIECE_BLACK && !engine_color) {
                    board_string += `<div class="possible_move_black" id="${x}_${y}" onclick="play(${x},${y})"></div>`
                } else if (player === PIECE_WHITE && engine_color) {
                    board_string += `<div class="possible_move_white" id="${x}_${y}" onclick="play(${x},${y})"></div>`
                }
            }
            board_string += '</div>'
        }
        board_string += '</div>'
    }
    document.getElementById("board").innerHTML = board_string;
}


function play(x, y) {
    /**
     * This function place piece i the board
     * @param x - the x coordinate of the move
     * @param y - the y coordinate of the move
     * */
    fetch(API_ENGINE_MOVE, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Credentials": true,
        },
        body: JSON.stringify({"x": x, "y": y})
    }).then(r => {
        return r;
    })
}


function update_score(score_black, score_white) {
    /**
     This function update the score of the game
     @param score_black - the number of black pieces on the board
     @param score - white: the number of white pieces on the board
     @return: null
     */
    // update the score
    document.getElementById("score_black").innerHTML = score_black
    document.getElementById("score_white").innerHTML = score_white

    // update the bar
    document.getElementById("bar_black").style.width = (score_black / (score_black + score_white) * 100) + "%"
    document.getElementById("bar_white").style.width = (score_white / (score_black + score_white) * 100) + "%"
}


function update_history(history) {
    /**
     * This function update the game history
     * @param history - The history of the game as json
     */
    let history_string = ""
    let last = "0"
    let piece
    let style_bolder = "font-weight: bold;"
    let style_italic = ""

    let y_chart = []
    let x_chart = []

    for (let i in history) {

        history_string += '<li class="move_li">'

        // history black
        if (history[i]["score"][0] === history[last]["score"][0]) {
            history_string += '<span class="move_info_score_left">&nbsp</span>'
        } else if (history[i]["score"][0] > history[last]["score"][0]) {
            history_string += `<span class="move_info_score_left" style="${style_bolder}"> +${history[i]["score"][0] - history[last]["score"][0]} </span>`
        } else {
            history_string += `<span class="move_info_score_left" style="${style_italic}"> ${history[i]["score"][0] - history[last]["score"][0]} </span>`
        }

        // move
        if (i === "0") {
            history_string += '<span class="move_info"> Middle </span>'
        } else {
            if (history[i]["player"] === PIECE_BLACK) {
                piece = "Black"
            } else {
                piece = " White"
            }
            history_string += `<span class="move_info"> ${piece}: ${history[i]["move"][0]} | ${history[i]["move"][1]}</span>`
        }


        // history White
        if (history[i]["score"][1] === history[last]["score"][1]) {
            history_string += '<span class="move_info_score_right">&nbsp</span>'
        } else if (history[i]["score"][1] > history[last]["score"][1]) {
            history_string += `<span class="move_info_score_right" style="${style_bolder}"> +${history[i]["score"][1] - history[last]["score"][1]} </span>`
        } else {
            history_string += `<span class="move_info_score_right" style="${style_italic}"> ${history[i]["score"][1] - history[last]["score"][1]} </span>`
        }

        history_string += "</li>"

        last = i

        y_chart.push(history[i]["score"][0] / (history[i]["score"][1] + history[i]["score"][0]) * 100);
        x_chart.push(i);
    }

    document.getElementById("history").innerHTML = history_string

    // update the chart
    game_old.data.labels = x_chart;
    game_old.data.datasets[0].data = y_chart;
    game_old.update();
}


function update_advice() {
    /**
     * This function update the visibility of advice
     */
    advice = !advice; // update the advice statement
    // update the button
    if (advice) {
        document.getElementById("button_advice").innerHTML = "Hide <i>advice</i>"
    } else {
        document.getElementById("button_advice").innerHTML = "Show <i>advice</i>"
    }

    const source_update = new EventSource(STREAM_API_BOARD);

    source_update.onmessage = function (event) {
        const stream_data = JSON.parse(JSON.stringify(event.data))
        let dataReceived = JSON.parse(stream_data)

        plot_board(dataReceived["move_board"], dataReceived["player"]);

        source_update.close();
    };
}


function change_engine_color() {
    /**This function change the color of the engine
     * */
    engine_color = !engine_color;

    fetch(API_SETTING, {
        method: "post",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"setting": "change_engine_color"})
    }).then(r => {
        return r
    })

    // engine color == black
    if (engine_color) {
        document.getElementById("button_play_as").innerHTML = "Play as <i>black</i>"
    } else {
        document.getElementById("button_play_as").innerHTML = "Play as <i>white</i>"
    }

}


function restart() {
    /** This function restart the current game
     * */
    fetch(API_SETTING, {
        method: "post",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"setting": "restart"})
    }).then(r => {
        return r;
    })
}

// stream the board
const source = new EventSource(STREAM_API_BOARD);

source.onmessage = function (event) {
    const stream_data = JSON.parse(JSON.stringify(event.data))
    let dataReceived = JSON.parse(stream_data)

    update_score(dataReceived["score_black"], dataReceived["score_white"]);
    plot_board(dataReceived["move_board"], dataReceived["player"]);
    update_history(dataReceived["history"])

    // update who plays
    if (dataReceived["player"] === PIECE_BLACK) {
        document.getElementById("info_title_left").innerHTML = "<b style='text-decoration: underline;'>Black</b>"
        document.getElementById("info_title_right").innerHTML = "White"
    } else {
        document.getElementById("info_title_left").innerHTML = "Black"
        document.getElementById("info_title_right").innerHTML = "<b style='text-decoration: underline;'>White</b>"
    }
};