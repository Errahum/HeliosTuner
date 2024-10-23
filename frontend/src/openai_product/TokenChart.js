import React, { useEffect, useRef } from 'react';
import { Chart } from 'chart.js/auto';

const TokenChart = () => {
    const chartRef = useRef(null);

    // Function to get month names
    const getMonthNames = () => {
        const months = [];
        for (let i = 0; i < 12; i++) {
            const date = new Date(0, i);
            months.push(date.toLocaleString('default', { month: 'long' }));
        }
        return months;
    };

    useEffect(() => {
        const ctx = chartRef.current.getContext('2d');
        const tokenChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: getMonthNames(), // Use the dynamically generated month names
                datasets: [{
                    label: 'Tokens Used',
                    data: Array(12).fill(0), // Initial data set to 0
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Month'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Tokens Used'
                        },
                        beginAtZero: true
                    }
                }
            }
        });

        return () => {
            tokenChart.destroy();
        };
    }, []);

    return (
        <canvas ref={chartRef} width="400" height="200"></canvas>
    );
};

export default TokenChart;