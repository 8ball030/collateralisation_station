<script>
	export let title;
	export let description;
	export let icon;
</script>

<div class="text-center px-12">
	<div class="mb-4">
		<i class={`fas ${icon} fa-2x`} style="color: #9F7AEA;"></i>
	</div>
	<h2 class="text-l font-semibold">{title}</h2>
	<p class="mt-2 text-sm">
		{description}
	</p>
</div>

<style>
</style>
