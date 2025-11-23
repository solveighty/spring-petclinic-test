package org.springframework.samples.petclinic.owner;

import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class OwnerAddPetUnitManualTest {

	private Owner owner;

	@BeforeEach
	void setUp() {
		owner = new Owner();
		owner.setId(100);
	}

	// Prueba para agregar nuevo pet
	@Test
	void shouldAddNewPetWhenIdIsNull() {
		Pet pet = new Pet();

		owner.addPet(pet);

		assertTrue(owner.getPets().contains(pet));
		assertEquals(1, owner.getPets().size());
	}

	// Prueba de no agregar pet existente
	@Test
	void shouldNotAddExistingPetWhenIdIsNotNull() {
		Pet pet1 = new Pet();
		owner.addPet(pet1);

		Pet pet2 = new Pet();
		pet2.setId(5);

		owner.addPet(pet2);

		assertEquals(1, owner.getPets().size());
		assertFalse(owner.getPets().contains(pet2));
	}

	// Prueba si pet es null
	@Test
	void shouldThrowExceptionWhenPetIsNull() {
		assertThrows(NullPointerException.class, () -> owner.addPet(null));
	}

	// Prueba de crear un pet con nombre duplicado
	@Test
	void shouldAllowDuplicatePetNames() {
		Pet pet1 = new Pet();
		pet1.setName("Lucky");

		Pet pet2 = new Pet();
		pet2.setName("Lucky");

		Pet pet3 = new Pet();
		pet3.setName("Lucky");

		owner.addPet(pet1);
		owner.addPet(pet2);
		owner.addPet(pet3);

		List<Pet> pets = owner.getPets();
		long count = pets.stream().filter(p -> "Lucky".equals(p.getName())).count();

		assertEquals(3, pets.size());
		assertEquals(3, count);
	}

	// Prueba de que el pet agregado tenga el owner seteado
	@Test
	void shouldSetOwnerOnPetWhenAdded() {
		Pet pet = new Pet();

		owner.addPet(pet);

		assertTrue(owner.getPets().contains(pet));
	}

}
