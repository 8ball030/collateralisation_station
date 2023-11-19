<script>
	import '../app.postcss';
	import { AppShell, AppBar, ConicGradient } from '@skeletonlabs/skeleton';
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	import { createWeb3Modal, defaultWagmiConfig } from '@web3modal/wagmi';
	import { getWeb3Details, readContract } from '$lib/utils';
	import Landing from '$lib/components/Landing.svelte';
	import toxAbi from '$lib/abis/tox.json';
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

	import './styles.css';

	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

	/**
	 * switch views
	 */
	$: isApp = false;
	function launch() {
		isApp = true;
	}

	/**
	 * wallet connect modal configs
	 */
	const chains = [mainnet, gnosis, sepolia, polygon, filecoin, filecoinCalibration];
	const projectId = '1b0aad06235a3007b00055160c73fe1d';
	const wagmiConfig = defaultWagmiConfig({
		chains,
		projectId
	});
	const modal = createWeb3Modal({ wagmiConfig, projectId, chains, themeMode: 'dark' });

	const contractAddress = '0xeB49bE5DF00F74bd240DE4535DDe6Bc89CEfb994';
	const olsContact = '0xc096362fa6f4A4B1a9ea68b1043416f3381ce300';

	let available = 1;

	onMount(async () => {
		const data = await readContract(abi, contractAddress, 'profit');
		console.log('data', data);
		available = data;
	});
	$: used = (3 / Number(-available)) * 100;

	/**
	 * stats chart configs
	 */
	const conicStops = [
		{ label: 'Available', color: 'rgba(255,255,255,1)', start: 0, end: used },
		{ label: 'Landed', color: 'rgba(255,255,255,0.5)', start: used, end: 100 }
	];
</script>

{#if isApp}
	<AppShell>
		<svelte:fragment slot="header">
			<AppBar background="bg-[#082341]">
				<svelte:fragment slot="lead">
					<h3>COLLATERALIZATION STATION</h3>
				</svelte:fragment>
				<svelte:fragment slot="trail">
					<div class="connect-btn">
						<w3m-button label="Connect" />
					</div>
				</svelte:fragment>
			</AppBar>
		</svelte:fragment>
		<svelte:fragment slot="sidebarLeft">
			<div id="sidebar-left" class="side">
				<div>
					<h3 class="mt-4">Balances</h3>
					<div>Available to Lend: ${-available}</div>
					<div>Lent: ${used}</div>
					<div class="divider"></div>
				</div>
				<div>
					<h3 class="mt-4">Portfolio</h3>
					<div>Loan Portfolio: 1000</div>
					<div>Collaterized NFTs: 400</div>
				</div>
				<div class="mt-4">
					<ConicGradient stops={conicStops} legend></ConicGradient>
				</div>
			</div>
		</svelte:fragment>
		<slot />
	</AppShell>
{:else}
	<Landing {launch} />
{/if}

<style>
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
