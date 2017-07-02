'use strict';

const ROUTES = [ 1, 2 ];
const dummy = [
  [{"duration": 1163, "distance": "13.2 mi", "timestamp": "1498950182"}, {"duration": 1163, "distance": "13.2 mi", "timestamp": "1498950782"}, {"duration": 1193, "distance": "13.2 mi", "timestamp": "1498951382"}, {"duration": 1211, "distance": "13.2 mi", "timestamp": "1498951982"}, {"duration": 1204, "distance": "13.2 mi", "timestamp": "1498952582"}],
  [{"duration": 1263, "distance": "14.8 mi", "timestamp": "1498952641"}]
];

function handleError(err) {
  console.error('Encountered an error while displaying the data');
  console.error(err);
}

function formatApiData(data) {
  return data.map((datapoint) => {
    const timestamp = new Date(datapoint.timestamp * 1000);

    return [
      timestamp,
      datapoint.duration
    ];
  });
}

function padData(data) {
  const targetData = data[0];
  const targetLength = 144 - data.length;
  const result = [];
  const tenMinutes = 60 * 10;

  for (let i = 0; i < targetLength; i += 1) {
    result.push({
      distance: targetData.distance,
      duration: targetData.duration,
      timestamp: parseInt(targetData.timestamp, 10) - (tenMinutes * (i+1))
    });
  }

  return result.concat(data);
}


function fetchData() {
  const result = ROUTES.map(id =>
    fetch(`/api/v1/routes/${id}/day`)
    .then(data => data.json())
    .then(data => data.data)
//    .then(data => dummy[id - 1])  // DUMMY DATA
    .then(padData)
  );

  return Promise.all(result);
}

function naiveMerge(allData) {
  const result = [];

  allData.forEach((allRouteData, routeId) => {
    allRouteData.forEach((datapoint, index) => {
      if (result[index] === undefined) {
        result[index] = [new Date(datapoint.timestamp * 1000)];
      }

      result[index] = result[index].concat(datapoint.duration);
    });
  });

  return result;
}

function fetchRouteData() {
  return fetch('/api/v1/routes')
  .then(data => data.json())
  .then(data => data.data);
}

function formatRouteData(routeData) {
  return routeData.map((item) => {
    return item.name;
  });
}

function convertToMinutes(x) {
  return (parseInt(x,10) / 60).toFixed(2);
}

function graphData([trafficData, routeData]) {
  const g = new Dygraph(
    document.getElementById('graph-container'),
    trafficData,
    {
      axes: {
        y: {
          axisLabelFormatter: convertToMinutes,
          valueFormatter: convertToMinutes
        }
      },
      labels: ['Time'].concat(routeData),
      legend: 'always',
      showRangeSelector: true,
      xlabel: 'Time',
      xValueParser: (x) => (1000 * parseInt(x, 10)),
      ylabel: 'Trip Duration (minutes)'
    });
}

Promise.all([
    fetchData().then(naiveMerge),
    fetchRouteData().then(formatRouteData)
])
.then(graphData)
.catch(handleError);
