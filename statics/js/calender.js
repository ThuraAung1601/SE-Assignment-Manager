var days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
const calendarDiv = document.querySelector('.calendar');
const eventTitle = document.getElementById("event-title");
const eventDescription = document.getElementById("event-description");
const eventStart = document.getElementById("event-start");
const eventEnd = document.getElementById("event-end");
const eventLocation = document.getElementById("event-location");

function generateCalendarBody() {
    calendarDiv.innerHTML = ''; // Clear any existing content

    const table = document.createElement('table');
    
    const thead = document.createElement('thead');
    const trHead = document.createElement('tr');

    const btnTdPrev = document.createElement('td');
    btnTdPrev.className = 'btn-td';
    const prevButton = document.createElement('span');
    prevButton.id = 'prev';
    prevButton.textContent = '<';
    btnTdPrev.appendChild(prevButton);
    trHead.appendChild(btnTdPrev);

    const monthTd = document.createElement('td');
    monthTd.setAttribute('colspan', '5');
    monthTd.id = 'month-name';
    trHead.appendChild(monthTd);

    const btnTdNext = document.createElement('td');
    btnTdNext.className = 'btn-td';
    const nextButton = document.createElement('span');
    nextButton.id = 'next';
    nextButton.textContent = '>';
    btnTdNext.appendChild(nextButton);
    trHead.appendChild(btnTdNext);

    thead.appendChild(trHead);

    const trDays = document.createElement('tr');
    days.forEach(day => {
        const td = document.createElement('td');
        td.textContent = day;
        trDays.appendChild(td);
    });
    thead.appendChild(trDays);

    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    tbody.id = 'tbody';
    table.appendChild(tbody);

    calendarDiv.appendChild(table);
}

generateCalendarBody();

let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();
const monthName = document.getElementById("month-name");
const tbody = document.getElementById("tbody");

function show_month(month) {
    const daysOfMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    const startDay = new Date(currentYear, month, 1).getDay();
    const totalDays = daysOfMonth[month];
    monthName.innerText = `${month + 1} / ${currentYear}`;
    tbody.innerHTML = '';

    let day = 1;
    let weeksInMonth = Math.ceil((totalDays + startDay) / 7);
    for (let i = 0; i < weeksInMonth; i++) {
        let tr = document.createElement("tr");
        for (let j = 0; j < 7; j++) {
            let td = document.createElement("td");
            if (i === 0 && j < startDay) {
                td.innerHTML = '';
            } else if (day <= totalDays) {
                td.innerHTML = day;
                td.addEventListener("click", () => fetchEventDetails(day, month, currentYear));
                day++;
            }
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }
}

function fetchEventDetails(day, month, year) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    
    fetch(`/events/${dateStr}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                eventTitle.textContent = "No event found";
                eventDescription.textContent = "";
                eventStart.textContent = "";
                eventEnd.textContent = "";
                eventLocation.textContent = "";
            } else {
                eventTitle.textContent = data.title;
                eventDescription.textContent = data.description;
                eventStart.textContent = data.start;
                eventEnd.textContent = data.end;
                eventLocation.textContent = data.location;
            }
        })
        .catch(error => console.error('Error fetching event details:', error));
}

document.getElementById("prev").addEventListener("click", () => {
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    show_month(currentMonth);
});

document.getElementById("next").addEventListener("click", () => {
    currentMonth = (currentMonth === 11) ? 0 : currentMonth + 1;
    show_month(currentMonth);
});

show_month(currentMonth);
