function toggleSelectionOnOdds(button){
    const matchId = button.getAttribute('data-match-id');
    const team_selection = button.getAttribute('data-team-selection');

    console.log("Match ID: " + matchId);
    console.log("Team Selection: " + team_selection);

    // Remove other selected buttons from this Match        
    document.querySelectorAll(`[data-match-id="${matchId}"]`).forEach(btn => {
        btn.classList.remove('selected');
    }); 
    // Make the button look selected
    button.classList.add('selected');
}

function clearBets(match_id){
    console.log("Clearing bets for match ID: " + match_id);
    if (match_id == null) match_id = 0;
    document.querySelectorAll('.bet-button').forEach(btn => {

        if (btn.classList.contains('selected'))
        {
            btn.classList.remove('selected');
        }
    });

    // const label = document.getElementById(`custom_bet_${match_id}`);
    // if (!label) {
    //     console.error(`Label with id custom_bet_${match_id} not found.`);
    //     return;
    // }
    // // Find the parent div of the label
    // const parentDiv = label.closest('div');
    // if (!parentDiv) {
    //     console.error('Parent div not found.');
    //     return;
    // }

    // Find the checkbox inside the same div
    const radio5 = document.getElementById(`bet_amount_5_${match_id}`);
    radio5.checked = false;
    const radio10 = document.getElementById(`bet_amount_10_${match_id}`);
    radio10.checked = false;
    const radio25 = document.getElementById(`bet_amount_25_${match_id}`);
    radio25.checked = false;
    const radioCustom = document.getElementById(`custom_bet_${match_id}`);
    radioCustom.checked = false;
}

function submitBets() {
    const bets = [];
    document.querySelectorAll('.bet-button.selected').forEach(btn => {
        // Retrieve match details and user selections
        const matchId = btn.getAttribute('data-match-id');
        const teamSelection = btn.getAttribute('data-team-selection');
        const oddsText = btn.textContent.trim();
        const betOdds = parseFloat(oddsText.replace('$', ''));
        const bet_home_odds = document.querySelectorAll(`#home_odds_${matchId}`)[0].textContent.trim();
        const bet_away_odds = document.querySelectorAll(`#away_odds_${matchId}`)[0].textContent.trim();
        const bet_draw_odds = document.querySelectorAll(`#draw_odds_${matchId}`)[0].textContent.trim();
        // Determine the selected bet amount
        const betAmountGroup = document.querySelector(`#bet_amount_group_${matchId}`);
        console.log(betAmountGroup);
        const selectedAmount = betAmountGroup.querySelector('input[type="radio"]:checked');
        let betAmount = selectedAmount ? parseFloat(selectedAmount.value) : 0;

        // If "Custom" is selected, retrieve the custom bet amount
        if (selectedAmount && selectedAmount.id === `custom_bet_${matchId}`) {
            const customInput = document.querySelector(`#custom_bet_amount_${matchId}`);
            betAmount = customInput ? parseFloat(customInput.value) : 0;
        }

        // Validate the bet amount
        if (!betAmount || betAmount <= 0) {
            alert(`Please enter a valid bet amount for Match ID ${matchId}: ${teamSelection}`);
            return;
        }

        // Add the bet details to the array
        bets.push({
            match_id: matchId,
            team_choice: teamSelection,
            bet_home_odds: bet_home_odds,
            bet_away_odds: bet_away_odds,
            bet_draw_odds: bet_draw_odds,
            bet_amount: betAmount,
            payout: (betAmount * betOdds).toFixed(2) // Calculate potential payout
        });
    });

    if (bets.length === 0) {
        alert("No bets selected. Please select a team and enter a bet amount.");
        return;
    }

    console.log(bets); // Debugging: View the constructed bets array
    
    // CSRF token for secure POST request
    const csrftoken = getCookie('csrftoken');
    fetch('/bets/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ bets }), // Send bets array as JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        bets.forEach(bet => clearBets(bet.match_id)) // Clear selections and reset input fields after submission
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Show custom input field when "Custom" is selected
function toggleCustomInput(matchId) {
    const customInput = document.getElementById(`custom_bet_amount_${matchId}`);
    const customRadio = document.getElementById(`custom_bet_${matchId}`);
    if (customRadio.checked) {
        customInput.style.display = 'block';
        customInput.focus();
    } else {
        customInput.style.display = 'none';
    }
}

// Helper to toggle bet selection
function toggleSelection(button) {
    // Allow only one selection per match
    const matchId = button.getAttribute('data-match-id');
    document.querySelectorAll(`.bet-button[data-match-id="${matchId}"]`).forEach(btn => {
        btn.classList.remove('selected');
    });

    // Toggle the current button
    button.classList.toggle('selected');
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}