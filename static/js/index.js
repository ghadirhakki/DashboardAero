//Adding a function to fetch data and return a response

async function getData(url) {
    const res = await axios.get(url);

    return await res.data;
}
function showProjects() {
    fetch('/projects/')
        .then(response => response.json())
        .then(data => {
            const projectList = document.getElementById('project-list');
            projectList.innerHTML = ''; // Clear previous content
            data.forEach(project => {
                const projectItem = document.createElement('li');
                projectItem.textContent = project.name;
                projectItem.addEventListener('click', () => {
                    showPhases(project.reference);
                });
                projectList.appendChild(projectItem);
            });
        })
        .catch(error => console.error('Error fetching projects:', error));
}

showProjects();