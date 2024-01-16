<script lang="ts">
    import { onMount } from 'svelte';
    import type { UNData } from '../types';

    let data: UNData[] = [];

    async function fetchData(): Promise<void> {
        console.log('Fetching data...');
        const url = 'http://localhost:8000/un_data';
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            data = await response.json();
            console.log('Data received:', data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    onMount(() => {
        fetchData();
    });
</script>

<!-- The rest of your component's HTML goes here -->
{#if data.length > 0}
    <div>
        <p>Country: {data[0].country_name}</p>
        <p>Year: {data[0].year}</p>
        <p>Statistic: {data[0].statistic_type}</p>
        <p>Value: {data[0].value}</p>
    </div>
{:else}
    <p>Loading data or no data available...</p>
{/if}