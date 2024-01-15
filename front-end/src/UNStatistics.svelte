<script lang="ts">
    import { onMount } from 'svelte';
    import type { UNData } from './types';

    let data: UNData[] = [];

    async function fetchData(): Promise<void> {
        const url = 'http://localhost:8000/un_data';
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            data = await response.json();
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    onMount(() => {
        fetchData();
    });
</script>

{#each data as item (item.country_id)}
    <div>
        <p>Country: {item.country_name}</p>
        <p>Year: {item.year}</p>
        <p>Statistic: {item.statistic_type}</p>
        <p>Value: {item.value}</p>
    </div>
{/each}