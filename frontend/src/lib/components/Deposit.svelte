<script>
	import { TOKENS_BY_SYMBOL_MAP } from '$lib/config/tokens';
	import { TabGroup, Tab } from '@skeletonlabs/skeleton';
	import DepositWidget from '$lib/components/DepositWidget.svelte';
	import { getWeb3Details, writeContract } from '$lib/utils';
	import { abi } from '../../../../onchain/abis/Collateral.json';
	import { waitForTransaction, fetchBalance, sendTransaction } from '@wagmi/core';
	import { onMount } from 'svelte';

	let tabSet = 0;
	let currency = 'USDC';
	let data;

	let isLoading = false;
	let isSuccess = false;

	const { chainId, account } = getWeb3Details();
	const contractAddress = '0xeB49bE5DF00F74bd240DE4535DDe6Bc89CEfb994';

	$: if (data && data.hash) {
		let res = waitForTransaction({
			hash: data?.hash
		});
		isLoading = res.isLoading;
		isSuccess = res.isSuccess;
	}

	function onCurrencySelect(curr) {
		currency = curr;
	}
	// States
	$: valueInput = 0;
	$: currencyInput = currency;
	// Derived states and logic
	$: tokenObj = TOKENS_BY_SYMBOL_MAP[chainId]?.[currencyInput];

	function onAmountInput(event) {
		valueInput = event.target.value;
	}

	async function handleDeposit() {
		// send transaction with wallet
		// const { hash } = await sendTransaction({
		// 	chainId: chainId,
		// 	to: contractAddress,
		// 	value: parseEther(valueInput)
		// });
		let res = await writeContract(abi, contractAddress, 'deposit', [tokenObj?.address, valueInput]);
		console.log('res_', res);
		data = res?.hash;
	}

	onMount(async () => {
		const data = await fetchBalance({
			address: '0x18070D824952Fb5d46F529659BdB497ebB1C5985'
		});
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
								<DepositWidget
									{onAmountInput}
									currency={currencyInput}
									{onCurrencySelect}
									bind:value={valueInput}
									supportLabel=""
								/>
							</div>
						</div>
					</div>
				{:else}
					<div class="auto-column">
						<div class="input-wrapper">
							<div class="link">
								<a href="https://app.pwn.xyz/#/create-loan"> Borrow on PWN </a>
							</div>
						</div>
					</div>
				{/if}
			</svelte:fragment>
		</TabGroup>

		{#if !account}
			Connect first
		{:else}
			<div>
				<button
					disabled={!valueInput || isLoading}
					on:click={handleDeposit}
					class="btn btn-dep w-full mt-4"
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
	.btn-dep {
		background: black;
		color: white;
	}
	.btn-dep:disabled {
		background: rgb(170, 170, 170);
		color: rgb(61, 61, 61);
	}
	.tab-text {
		font-size: 12px;
		font-weight: 500;
	}
	.input-wrapper {
		position: relative;
		border: 1px solid rgb(34, 39, 46);
		border-radius: 20px;
		width: 400px;
	}
	.input-section {
		border-radius: 12px;
		color: grey;
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
		border: 0.5px solid grey;
	}
	.link {
		padding: 20px;
		height: 120px;
		font-weight: 600;
		color: #3396ff;
	}
</style>
