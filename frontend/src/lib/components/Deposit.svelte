<script>
	import { TOKENS_BY_SYMBOL_MAP } from '$lib/config/tokens';
	import { TabGroup, Tab } from '@skeletonlabs/skeleton';
	import Swap from '$lib/components/Swap.svelte';
	import { getWeb3Details, writeContract } from '$lib/utils';
	import { abi } from '../../../../onchain/artifacts/contracts/Collateral.sol/Collateral.json';
	import { waitForTransaction, fetchBalance } from '@wagmi/core';
	import { onMount } from 'svelte';
	import getBalances from '$lib/actions/getBalances';

	let tabSet = 0;
	let currency = 'DAI';
	let data;

	let isLoading = false;
	let isSuccess = false;

	const { chainId, account } = getWeb3Details();
	const contractAddress = '0x..';

	function handleDeposit(val) {
		let res = writeContract(abi, contractAddress, 'deposit');
		data = res.data;
		write = res.write;
	}

	$: if (data && data.hash) {
		let res = waitForTransaction({
			hash: data?.hash
		});
		isLoading = res.isLoading;
		isSuccess = res.isSuccess;
	}

	function onCurrencySelect(val) {
		console.log('selected');
		currency = val;
	}

	function setValue() {
		console.log('set');
	}

	// States
	let inputAmount = 0;
	$: input = currency;

	console.log(input);
	// Derived states and logic
	const inputToken = TOKENS_BY_SYMBOL_MAP[chainId]?.[input];

	console.log('inputToken', inputToken);
	// add prices
	const depositPrice = 1.0;

	onMount(async () => {
		const data = await fetchBalance({
			address: '0x18070D824952Fb5d46F529659BdB497ebB1C5985'
		});
		//const balance = await getBalances();

		console.log(data);
		console.log(data?.formatted);
		console.log(data?.symbol);
	});
</script>

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
									setValue
									currency={input}
									{onCurrencySelect}
									bind:value={inputAmount}
									supportLabel=""
								/>
							</div>
						</div>
					</div>
				{:else}
					<div class="auto-column">
						<div class="input-wrapper">Redirect to PWN</div>
					</div>
				{/if}
			</svelte:fragment>
		</TabGroup>

		{#if !account}
			Connect first
		{:else}
			<div>
				<button
					disabled={!inputAmount || isLoading}
					onClick={() => handleDeposit()}
					class="btn variant-ringed-primary w-full mt-4"
				>
					{isLoading ? 'Deposit...' : 'Deposit'}
				</button>

				{#if isSuccess}
					<div>
						Successfully deposited!
						<div>
							<a href={`https://etherscan.io/tx/${data?.hash}`}>Etherscan</a>
						</div>
					</div>
				{/if}
			</div>
		{/if}
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
</style>
