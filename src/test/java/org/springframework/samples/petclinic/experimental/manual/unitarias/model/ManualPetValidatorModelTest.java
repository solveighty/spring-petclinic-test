
package org.springframework.samples.petclinic.experimental.manual.unitarias.model;

import java.time.LocalDate;

import org.springframework.samples.petclinic.owner.Pet;
import org.springframework.samples.petclinic.owner.PetType;
import org.springframework.samples.petclinic.owner.PetValidator;
import org.springframework.validation.BeanPropertyBindingResult;
import org.springframework.validation.Errors;

public class ManualPetValidatorModelTest {

	public static void main(String[] args) {

		PetValidator validator = new PetValidator();

		System.out.println("=========== TEST PetValidator.validate() ===========");

		// Caso 1: Nombre vacío
		System.out.println("\nCaso 1 - Nombre vacío:");
		logValidationErrors(createPet("", new PetType(), LocalDate.now(), true), validator);

		// Caso 2: Nombre con espacios
		System.out.println("\nCaso 2 - Nombre con espacios:");
		logValidationErrors(createPet("   ", new PetType(), LocalDate.now(), true), validator);

		// Caso 3: Nombre válido
		System.out.println("\nCaso 3 - Nombre válido:");
		logValidationErrors(createPet("Lucky", new PetType(), LocalDate.now(), true), validator);

		// Caso 4: Pet nuevo sin tipo
		System.out.println("\nCaso 4 - Pet nuevo sin tipo:");
		logValidationErrors(createPet("Lucky", null, LocalDate.now(), true), validator);

		// Caso 5: Pet existente sin tipo (isNew false)
		System.out.println("\nCaso 5 - Pet existente sin tipo:");
		Pet existing = createPet("Lucky", null, LocalDate.now(), false);
		existing.setId(5);
		logValidationErrors(existing, validator);

		// Caso 6: Fecha nula
		System.out.println("\nCaso 6 - Fecha nula:");
		logValidationErrors(createPet("Lucky", new PetType(), null, true), validator);

		// Caso 7: Todo nulo
		System.out.println("\nCaso 7 - Todo nulo:");
		logValidationErrors(createPet(null, null, null, true), validator);

		// Caso 8: Objeto null
		System.out.println("\nCaso 8 - Objeto null:");
		try {
			validator.validate(null, null);
			System.out.println("❌ No ocurrió error (¿debería?)");
		}
		catch (Exception e) {
			System.out.println("✅ Error lanzado: " + e.getClass().getSimpleName());
		}
	}

	private static Pet createPet(String name, PetType type, LocalDate birthDate, boolean isNew) {
		Pet pet = new Pet();
		pet.setName(name);
		pet.setType(type);
		pet.setBirthDate(birthDate);
		if (!isNew)
			pet.setId(10);
		return pet;
	}

	private static void logValidationErrors(Pet pet, PetValidator validator) {
		Errors errors = new BeanPropertyBindingResult(pet, "pet");
		validator.validate(pet, errors);

		if (errors.hasErrors()) {
			errors.getFieldErrors()
				.forEach(error -> System.out
					.println("Error → Campo: " + error.getField() + ", Código: " + error.getCode()));
		}
		else {
			System.out.println("✅ Sin errores");
		}
	}

}
