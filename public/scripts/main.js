'use strict';

function fetchData() {
  return fetch('/api/v1/routes/1/day')
  .then(data => data.json())
  .then(data => data.data);
}

function formatData(data) {
  const result = ['timestamp,duration\n'];

  data.forEach((datapoint) => {
    const timestamp = new Date(datapoint.timestamp * 1000);

    result.push(`${timestamp},${datapoint.duration}\n`);
  });

  return result.join('');
}

function graphData(data) {
  const g = new Dygraph(document.getElementById('graphdiv'), data);
}

fetchData()
.then(formatData)
.then(graphData);
