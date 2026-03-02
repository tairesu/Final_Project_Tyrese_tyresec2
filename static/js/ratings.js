let icons = document.querySelectorAll('#ratings svg');
let last_clicked_rating = 0;
let last_hovered_rating = "0";

function update_ratings(new_rating){
    let icon_index = new_rating - 1;
    icons.forEach((icon,i) => { 
        if (i <= icon_index) {
            // Brighten prior icons 
            icon.classList.add('active');
        } else {
            // Dim remaining icons
            icon.classList.remove('active');
        }
            
    });
}
function hover_prior_ratings(new_rating){
    // Grab the gear icon that was last hovered
    let icon_index = new_rating - 1;
    // Slightly illuminate all prior icons
    icons.forEach((icon,i) => { 
        if (i <= icon_index) {
            icon.classList.add('hovered');
        }
            
    });
}
function unhover_prior_ratings(){
    hovered_icons =  document.querySelectorAll("svg.rating-icon.hovered");
    if (hovered_icons.length > 0)
        hovered_icons.forEach((hovered_icon)=>{hovered_icon.classList.remove('hovered')});
}
