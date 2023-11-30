<script>
	import { getLogo } from '$lib/config/tokens';
	import CurrencySearch from '$lib/components/CurrencySearch.svelte';
	import { getWeb3Details } from '$lib/utils';

	export let currency;
	export let onCurrencySelect;
	export let onAmountInput;
	export let supportLabel;

	const { chainId } = getWeb3Details();

	let modalOpen = false;

	const handleClick = () => (modalOpen = true);

	const handleCurrencySelect = (selectedCurrency) => {
		onCurrencySelect(selectedCurrency);
		modalOpen = false;
	};
</script>

<div class="input-panel">
	<div class="input-row">
		<input
			class="token-input"
			on:change={onAmountInput}
			on:input={onAmountInput}
			type="text"
			pattern="^[0-9]*[.,]?[0-9]*$"
			minLength={1}
			maxLength={79}
		/>
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
		border: 1px solid #29a10a;
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
	.token-input {
		width: 0px;
		position: relative;
		font-weight: 500;
		outline: none;
		border: none;
		flex: 1 1 auto;
		background-color: transparent;
		font-size: 28px;
		overflow: hidden;
		text-overflow: ellipsis;
		text-align: left;
	}
</style>
