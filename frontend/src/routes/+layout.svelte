<script>
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	import { createWeb3Modal, defaultWagmiConfig } from '@web3modal/wagmi';
	import { getWeb3Details } from '$lib/utils';
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
</script>

<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				<h2 class="title">COLLATERALIZATION STATION</h2></svelte:fragment
			>
			<svelte:fragment slot="trail">
				<div class="connect-btn">
					<w3m-button label="Connect" />
				</div>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<slot />
</AppShell>

<style>
</style>
