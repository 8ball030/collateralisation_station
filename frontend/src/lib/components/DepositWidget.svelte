<!-- Swap.svelte -->
<script>
	import { getLogo } from '$lib/config/tokens';
	import Input from '$lib/components/Input.svelte';
	import CurrencySearch from '$lib/components/CurrencySearch.svelte';
	import { getWeb3Details } from '$lib/utils';

	export let currency;
	export let onCurrencySelect;
	export let value;
	export let setValue;
	export let supportLabel;

	const { chainId } = getWeb3Details();

	let modalOpen = false;

	const handleClick = () => {
		modalOpen = true;
	};

	const handleCurrencySelect = (selectedCurrency) => {
		onCurrencySelect(selectedCurrency);
		modalOpen = false;
	};
</script>

<div class="input-panel">
	<div class="input-row">
		<Input onUserInput={setValue} class="token-amount-input" bind:value disabled={false} />
		<div class="currency-select-container">
			<span>{supportLabel}</span>
			<button class="currency-select" on:click={handleClick}>
				<div class="aligner">
					<img class="logo" src={getLogo(currency, chainId) || '/dai.png'} alt="token" />
					<div class="input-row">{currency ? currency : 'Select Token'}</div>
				</div>
			</button>
		</div>
	</div>
	{#if modalOpen}
		<CurrencySearch {modalOpen} {handleCurrencySelect} />
	{/if}
</div>

<style>
	.logo {
		width: 1.5rem;
		height: 1.5rem;
		margin-right: 0.5rem;
	}
	.input-panel {
		display: flex;
		flex-direction: column;
		position: relative;
		border-radius: 20px;
		z-index: 1;
		height: 80px;
		padding: 20px;
		transition: height 1s ease;
		border: 1px solid #ae85a2;
		background-color: #e5e7eb;
		color: rgb(73, 74, 84);
	}
	.input-row {
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
		color: rgb(73, 74, 84);
	}
	.currency-select {
		align-items: center;
		background-color: #e5e7eb;
		opacity: 1;
		box-shadow: 5px 5px 5px #4d384842;
		color: white;
		cursor: pointer;
		border-radius: 20px;
		outline: none;
		user-select: none;
		border: none;
		font-size: 18px;
		font-weight: 535;
		height: 2.4rem;
		padding: 5px;
		justify-content: space-between;
		margin-left: 12px;
	}
	.currency-select:focus,
	.currency-select:hover {
		background-color: #4c38470a;
	}
	.aligner {
		display: flex;
		align-items: center;
		padding: 2px 4px;
		border-radius: 16px;
		justify-content: space-between;
		width: 100%;
	}
</style>
