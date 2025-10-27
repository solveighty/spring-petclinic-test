package org.springframework.samples.petclinic.owner;

public class ManualOwnerModelTest {

	public static void main(String[] args) {

		System.out.println("=========== TEST addPet() ===========");

		Owner owner = new Owner();

		// Caso 1: Creando pet nuevo
		Pet newPet = new Pet();
		System.out.println("\nCaso 1 - Pet nuevo (ID null):");
		owner.addPet(newPet);
		System.out.println("¿Se agregó? " + owner.getPets().contains(newPet));
		System.out.println("Cantidad de mascotas: " + owner.getPets().size());

		// Caso 2: Creando pet existente
		Pet existingPet = new Pet();
		existingPet.setId(5); // simula pet ya persistido
		System.out.println("\nCaso 2 - Pet existente (ID != null):");
		owner.addPet(existingPet);
		System.out.println("¿Se agregó? " + owner.getPets().contains(existingPet));
		System.out.println("Cantidad de mascotas: " + owner.getPets().size());

		// Caso 3: Creando pet null
		System.out.println("\nCaso 3 - Pet null:");
		try {
			owner.addPet(null);
			System.out.println("No ocurrió error (¿debería?)");
		}
		catch (Exception e) {
			System.out.println("Error lanzado: " + e.getClass().getSimpleName());
		}

		// Caso 4: Creando con el mismo nombre
		System.out.println("\nCaso 4 - Nombre duplicado:");
		Pet pet1 = new Pet();
		pet1.setName("Lucky");
		owner.addPet(pet1);

		Pet pet2 = new Pet();
		pet2.setName("Lucky");
		owner.addPet(pet2);

		System.out.println("Cantidad de mascotas: " + owner.getPets().size());
		System.out.println("¿Hay duplicado? "
				+ owner.getPets().stream().filter(p -> "Lucky".equals(p.getName())).count() + " con nombre Lucky");

		// Caso 5: Relación dueño-mascota
		System.out.println("\nCaso 5 - Relación bidireccional:");
		System.out.println("pet1 está en la colección del owner: " + owner.getPets().contains(pet1));
	}

}
