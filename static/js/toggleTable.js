function toggleTable(junkyardId, justshow = false) {
    const table = document.getElementById(`table-${junkyardId}`);
    const chevron = document.getElementById(`chevron-${junkyardId}`);
    
    if ( justshow || table.classList.contains('hidden')) {
        table.classList.remove('hidden');
        chevron.classList.add('chevron-opened');
        chevron.style.transform = 'rotate(0deg)';
    } else {
        table.classList.add('hidden');
        chevron.classList.remove('chevron-opened');
        chevron.style.transform = 'rotate(-180deg)';
    }
}