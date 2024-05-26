document.getElementById('nav-toggle').addEventListener('click', function () {
    const navLinksContainer = document.getElementById('nav-links-container');
    if (navLinksContainer.style.display === 'block') {
        navLinksContainer.style.display = 'none';
    } else {
        navLinksContainer.style.display = 'block';
    }
});

window.addEventListener('resize', function () {
    const navLinksContainer = document.getElementById('nav-links-container');
    const navLinks = document.getElementById('nav-links');
    const navToggle = document.getElementById('nav-toggle');

    if (window.innerWidth > 600) {
        navLinksContainer.style.display = 'none';
        navLinks.style.display = 'flex';
        navToggle.style.display = 'none';
    } else {
        navLinks.style.display = 'none';
        navToggle.style.display = 'block';
    }
});

// Initial check to set correct display properties
window.dispatchEvent(new Event('resize'));

// Password generator
const generatePassword = () => {
    const length = document.getElementById('password-length').value;
    const useUppercase = document.getElementById('uppercase').checked;
    const useLowercase = document.getElementById('lowercase').checked;
    const useNumbers = document.getElementById('numbers').checked;
    const useSymbols = document.getElementById('symbols').checked;

    const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const lowercase = 'abcdefghijklmnopqrstuvwxyz';
    const numbers = '0123456789';
    const symbols = '!@#$%^&*()_+[]{}|;:,.<>?';

    let allChars = '';
    if (useUppercase) allChars += uppercase;
    if (useLowercase) allChars += lowercase;
    if (useNumbers) allChars += numbers;
    if (useSymbols) allChars += symbols;

    let password = '';
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * allChars.length);
        password += allChars[randomIndex];
    }

    document.getElementById('generated-password').textContent = password;
};



document.getElementById('generate-password').addEventListener('click', () => {
    generatePassword();
    document.getElementById('password').value = document.getElementById('generated-password').textContent;
});

document.getElementById('copy-password').addEventListener('click', () => {
    const password = document.getElementById('generated-password').textContent;
    navigator.clipboard.writeText(password).then(() => {
        alert('Password copied to clipboard');
    });
});

const options = ['password-length', 'password-length-range', 'uppercase', 'lowercase', 'numbers', 'symbols'];

options.forEach(option => {
    document.getElementById(option).addEventListener('input', () => {
        generatePassword();
        document.getElementById('password').value = document.getElementById('generated-password').textContent;
    });
});

// Synchronize password length input and range
document.getElementById('password-length-range').addEventListener('input', (e) => {
    document.getElementById('password-length').value = e.target.value;
    generatePassword();
    document.getElementById('password').value = document.getElementById('generated-password').textContent;
});

document.getElementById('password-length').addEventListener('input', (e) => {
    document.getElementById('password-length-range').value = e.target.value;
    generatePassword();
    document.getElementById('password').value = document.getElementById('generated-password').textContent;
});

// Initial generation of the password if there is no existing password
if (!document.getElementById('password').value) {
    generatePassword();
    document.getElementById('password').value = document.getElementById('generated-password').textContent;
}
