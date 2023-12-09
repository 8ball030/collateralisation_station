<script>
	import '../app.postcss';
	import { AppShell, AppBar, ConicGradient } from '@skeletonlabs/skeleton';
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	import { createWeb3Modal, defaultWagmiConfig } from '@web3modal/wagmi';
	import { readContract } from '$lib/utils';
	import Landing from '$lib/components/Landing.svelte';
	import {
		mainnet,
		gnosis,
		sepolia,
		polygon,
		filecoin,
		filecoinCalibration
	} from '@wagmi/core/chains';
	import { onMount } from 'svelte';
	import { abi } from '../../../onchain/abis/Collateral.json';
	import { CONTRACTS, PROJECT_ID } from '$lib/constants';
	import './styles.css';

	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

	/**
	 * switch views
	 */
	$: isApp = false;
	const launch = () => (isApp = true);

	/**
	 * wallet connect modal configs
	 */
	const chains = [mainnet, gnosis, sepolia, polygon, filecoin, filecoinCalibration];
	const wagmiConfig = defaultWagmiConfig({
		chains,
		projectId: PROJECT_ID
	});
	const modal = createWeb3Modal({ wagmiConfig, projectId: PROJECT_ID, chains, themeMode: 'dark' });

	// TODO: get used from contract
	let used = 3;
	let total = 9;
	let available = total - used;
	let usedPer = (used / total) * 100;
	let availablePer = (available / total) * 100;

	onMount(async () => {
		const data = await readContract(abi, CONTRACTS.COLL, 'profit');

		total = Math.floor(Number(-data)) / 1000000000000000;
	});

	/**
	 * stats chart configs
	 */
	const conicStops = [
		{ label: 'Available', color: '#A6D35D', start: 0, end: availablePer },
		{ label: 'Lent', color: '#02455f', start: availablePer, end: 100 }
	];
</script>

{#if isApp}
	<AppShell>
		<h3 class="title">COLLATERALIZATION STATION</h3>
		<svelte:fragment slot="sidebarRight">
			<div id="sidebar-left" class="side">
				<div>
					<h3 class="mt-4">Balances</h3>
					<div>Available to Lend: ${available}</div>
					<div>Lent: ${used}</div>
					<div class="divider"></div>
				</div>
				<div class="mt-4">
					<ConicGradient stops={conicStops} legend></ConicGradient>
				</div>
			</div>
			<div class="connect-btn">
				<w3m-button label="Connect" />
			</div>
		</svelte:fragment>
		<slot />
	</AppShell>
{:else}
	<Landing {launch} />
{/if}

<style>
	.title {
		font-size: 45px;
		color: black;
		width: 100px;
		line-height: 43px;
		font-weight: 800;
	}
	.side {
		background: black;
		width: 300px;
		height: 100%;
		padding: 20px;
		color: #97b5bc;
		font-weight: 300;
		line-height: 34px;
	}
	.divider {
		border: 0.8px solid #97b5bc;
		margin-top: 5px;
	}
</style>
