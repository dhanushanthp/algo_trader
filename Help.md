## Y axis Annotation
```json
chart.addYaxisAnnotation({
    id: 'unique-id',
    y: 670,
    label: {
        text: 'Y-axis Annotation',
    }
})
```

## X Axis Pre Defined
```json
annotations: {
    xaxis: [{
        x: '<timestamp>',
        borderColor: '#00E396',
        label: {
            borderColor: '#00E396',
            style: {
                fontSize: '12px',
                color: '#fff',
                background: '#00E396'
            },
            orientation: 'horizontal',
            offsetY: 7,
            text: 'Annotation Test'
        }
    }]
}
```
