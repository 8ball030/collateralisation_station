<script>
	import LCard from './LCard.svelte';
	export let launch;
</script>

<div class="landing">
	<div class="h-full w-full cnt-top">
		<img src="/bg.png" class="bg" alt="bg" />
		<div class="text-right px-4 pt-8 pb-10 text-cnt">
			<h1 class="text-6xl font-semibold">COLLATERALIZATION STATION</h1>
			<p class="text-xl mt-4">Secure, collateralized service loans with</p>
			<button class="btn variant-ringed-primary w-full mt-6 launch" on:click={launch}
				>Launch App</button
			>
		</div>
	</div>
	<div class="flex justify-center items-center space-x-6 px-6 pt-8 pb-12 bg-[#0E0E33] cnt-bt">
		<LCard
			icon="fa-link"
			title="Liquidity via NFTs"
			description="Leverage NFTs for liquidity without selling, using Chainlink oracles for real-time valuation"
		/>
		<LCard
			icon="fa-chart-line"
			title="Data-Driven Loans"
			description="Tailored loan offers with flexible repayment or secure, automated liquidation processes"
		/>
		<LCard
			icon="fa-coins"
			title="Token-Powered Lending"
			description="Convert ERC20 tokens into interest-bearing assets for additional lending options"
		/>
	</div>
</div>

<style>
	.launch {
		width: 350px;
	}
	.launch:hover {
		background: #a6c0c82e;
	}
	.cnt-top {
		background: #210a42;
		overflow: hidden;
	}
	.text-cnt {
		position: fixed;
		top: 48px;
		right: 47px;
	}
	.landing {
		display: flex;
		height: 100%;
		flex-direction: column;
		justify-content: space-between;
	}
	.bg {
		width: 100%;
		transform: translate(0px, -51px);
		height: 122%;
	}
	.cnt-bt {
		gap: 20px;
	}
</style>
