<script>
	import '../app.postcss';
	import { AppShell, AppBar, ConicGradient } from '@skeletonlabs/skeleton';
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	import { createWeb3Modal, defaultWagmiConfig } from '@web3modal/wagmi';
	import { getWeb3Details } from '$lib/utils';
	import Landing from '$lib/components/Landing.svelte';

	import {
		mainnet,
		gnosis,
		sepolia,
		polygon,
		filecoin,
		filecoinCalibration,
		mantle,
		mantleTestnet,
		scrollSepolia,
		scrollTestnet
	} from '@wagmi/core/chains';

	import './styles.css';

	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

	$: isApp = false;

	function launch() {
		isApp = true;
	}

	console.log('isApp', isApp);

	const chains = [
		mainnet,
		gnosis,
		sepolia,
		polygon,
		filecoin,
		filecoinCalibration,
		mantle,
		mantleTestnet,
		scrollSepolia,
		scrollTestnet
	];
	const projectId = '1b0aad06235a3007b00055160c73fe1d';
	const wagmiConfig = defaultWagmiConfig({
		chains,
		projectId
	});
	const modal = createWeb3Modal({ wagmiConfig, projectId, chains, themeMode: 'dark' });

	const conicStops = [
		{ label: 'Available', color: 'rgba(255,255,255,1)', start: 0, end: 40 },
		{ label: 'Landed', color: 'rgba(255,255,255,0.5)', start: 40, end: 85 },
		{ label: 'Total', color: 'rgba(255,255,255,0.25)', start: 85, end: 100 }
	];
</script>

{#if isApp}
	<AppShell>
		<svelte:fragment slot="header">
			<AppBar background="bg-[#082341]">
				<svelte:fragment slot="lead">
					<img class="h-10" src="/lg.png" alt="lg" />
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
					<div>Available: 813</div>
					<div>Landed: 500</div>
					<div class="divider"></div>
					<div>Total: 1313</div>
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
