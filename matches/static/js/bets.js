function toggleSelection(button){
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