document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    if (path === '/' || path === '/home/') {
        document.getElementById('link-home')?.classList.add('active');
    } else if (path.includes('newlaunch')) {
        document.getElementById('link-new')?.classList.add('active');
    } else if (path.includes('oldlaunches')) {
        document.getElementById('link-old')?.classList.add('active');
    }
});
