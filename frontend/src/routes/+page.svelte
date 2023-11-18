<script>
	import { TOKENS_BY_SYMBOL_MAP } from '$lib/config/tokens';
	import { TabGroup, Tab } from '@skeletonlabs/skeleton';
	import Swap from '$lib/components/Swap.svelte';
	import { getWeb3Details } from '$lib/utils';

	let tabSet = 0;
	let currency = 'DAI';
	const { chainId, account } = getWeb3Details();

	function onCurrencySelect(val) {
		console.log('selected');
		currency = val;
	}

	let value = 10;
	function setValue() {
		console.log('set');
	}
	let supportLabel = 'label';

	// States
	let inputAmount = '';
	let outputAmount = '0';
	let borrowAmount = 0;
	let input = 'DAI';
	let output = 'OLAS';

	// Derived states and logic
	const inputToken = TOKENS_BY_SYMBOL_MAP[chainId]?.[input];
	const outputToken = TOKENS_BY_SYMBOL_MAP[chainId]?.[output];

	// add prices
	const depositPrice = 1.0;
	const borrowPrice = 1.0;
</script>

<div class="container">
	<div class="page-wrapper">
		<div class="leverage-wrapper dark">
			<TabGroup>
				<Tab bind:group={tabSet} name="tab1" value={0}>
					<span class="tab-text"> LEND </span>
				</Tab>
				<Tab class="tab-text" bind:group={tabSet} name="tab2" value={1}>
					<span class="tab-text"> BORROW </span>
				</Tab>
				<svelte:fragment slot="panel">
					{#if tabSet === 0}
						<div class="auto-column">
							<div class="input-wrapper">
								<div class="input-section">
									<Swap
										currency={input}
										{onCurrencySelect}
										bind:value={inputAmount}
										supportLabel=""
									/>
								</div>
								<div class="input-section">
									<Swap
										otherCurrency={input}
										currency={output}
										{onCurrencySelect}
										bind:value={borrowAmount}
										supportLabel=""
									/>
								</div>
							</div>
						</div>
					{:else}
						<div class="auto-column">
							<div class="input-wrapper">
								<div class="input-section">
									<Swap
										currency={input}
										{onCurrencySelect}
										bind:value={inputAmount}
										supportLabel=""
									/>
								</div>
								<div class="input-section">
									<Swap
										otherCurrency={input}
										currency={output}
										{onCurrencySelect}
										bind:value={borrowAmount}
										supportLabel=""
									/>
								</div>
							</div>
						</div>
					{/if}
				</svelte:fragment>
			</TabGroup>

			{#if !account}
				Connect first
			{:else}
				<button class="btn variant-ringed-primary w-full mt-4">Submit</button>
			{/if}
		</div>
	</div>
</div>

<style>
	.container {
		margin: auto;
		margin-top: 80px;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.tab-text {
		font-size: 12px;
		font-weight: 500;
	}

	.arrow-container {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
	}

	.input-wrapper {
		position: relative;
		background-color: #e5e7eb;
		border: 1px solid rgb(34, 39, 46);
		border-radius: 20px;
		width: 400px;
	}

	.input-section {
		background-color: #e5e7eb; /* Replace with actual theme color */
		border-radius: 12px;
		color: var(--neutral1); /* Replace with actual theme color */
		font-size: 14px;
		line-height: 20px;
		font-weight: 500;
		margin: 4px;
		min-height: 72px;
		padding: 16px;
		position: relative;
	}

	.input-section:before {
		box-sizing: border-box;
		background-size: 100%;
		border-radius: inherit;
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
		content: '';
		border: 0.5px solid var(--lighterSurface2); /* Use darken(-0.02, var(--surface2)) */
	}

	.slider-wrapper {
		position: absolute;
		width: 100%;
		top: 50%;
		transform: translateY(-50%);
		z-index: 99;
	}
</style>
