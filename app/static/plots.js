
const data1 = [{
  x: word_count,
  y: source_count,
  mode: 'markers',
  type: 'scatter',
  text: titles,
  marker: { size: 12 }
}];

const layout1 = {
  xaxis: {
    title: 'Log of Word Count',
    type: 'log',
    autorange: true
  },
  yaxis: {
    title: 'Log of Source Count',
    type: 'log',
    autorange: true

  },
  title: {text: 'Log of Source Count vs Log of Word Count'}
};


const data2 = [{
  x: word_count,
  y: image_count,
  mode: 'markers',
  type: 'scatter',
  text: titles,
  marker: { size: 12 }
}];

const layout2 = {
  xaxis: {
    title: 'Log of Word Count',
    type: 'log',
    autorange: true
  },
  yaxis: {
    title: 'Log of Image Count',
    type: 'log',
    autorange: true

  },
  title: {text: 'Log of Image Count vs Log of Word Count'}
};

const data3 = [{
  x: published,
  y: word_count,
  mode: 'markers',
  type: 'scatter',
  text: titles,
  marker: { size: 12 }
}];

const layout3= {
  xaxis: {
    title: 'Date Published',
    autorange: true
  },
  yaxis: {
    title: 'Log of Word Count',
    type: 'log',
    autorange: true
  },
  title: {text: 'Log of Word Count vs Date Published'}
};

const data4 = [{
  x: modified,
  y: word_count,
  mode: 'markers',
  type: 'scatter',
  text: titles,
  marker: { size: 12 }
}];

const layout4= {
  xaxis: {
    title: 'Last Date Modified',
    autorange: true
  },
  yaxis: {
    title: 'Log of Word Count',
    type: 'log',
    autorange: true
  },
  title: {text: 'Log of Word Count vs Last Date Modified'}
};

Plotly.newPlot('plot1', data1, layout1);
Plotly.newPlot('plot2', data2, layout2);
Plotly.newPlot('plot3', data3, layout3);
Plotly.newPlot('plot4', data4, layout4);
